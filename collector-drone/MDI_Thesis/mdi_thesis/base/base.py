"""
mdi_thesis base module.

If you want to replace this with a Flask application run:

    $ make init

and then choose `flask` as template.
"""
# from datetime import date
import json
from typing import Dict, List, Any
import requests
import mdi_thesis.constants as constants
import mdi_thesis.base.utils as utils
import logging
import os

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.CRITICAL)


class Request:
    """
    Class for GitHub Request
    """

    def __init__(self) -> None:
        self.token = constants.API_TOKEN
        self.results_per_page = 100
        self.headers = {"Authorization": "token " + self.token}
        self.session = requests.Session()
        self.response = requests.Response()
        self.selected_repos_dict = {}  # type: dict[int, dict]
        self.repository_dict = {}  # type: dict[int, list[dict[str, Any]]]
        # TODO: Move filepath to other location
        query_features_file = open(os.path.join(os.path.dirname(__file__), '..', 'query_features.json'), encoding="utf-8")
        self.query_features = json.load(query_features_file)

    def select_repos(
        self,
        repo_list: List[int],
        repo_nr: int = 100,
        language: str = "python",
        sort: str = "stars",
        order: str = "desc",
        help_wanted_issues: str = "True",
        
    ) -> List[Dict[str, Any]]:
        """
        Select Repositories according to Parameters
        :param repo_nr: Number of queried repositories.
        :param language: Programming language of queried repositories.
        :param sort: Factor by which the repositories are sorted.
        :param repo_list: List with repositories if preselected
        :returns: List with dictionaries of selected repositories
        """
        selected_repos = []
        if repo_list:
            for item in repo_list:
                url = f"https://api.github.com/repositories/{item}"
                response = self.session.get(
                    url, headers=self.headers, timeout=100)
                results = response.json()
                while "next" in response.links.keys():
                    res = self.session.get(
                        response.links["next"]["url"], headers=self.headers
                    )
                    results.extend(res.json())
                selected_repos.append(results)

        else:
            search_url = (
                "https://api.github.com/search/repositories?q=language:"
                + language
                + "&sort="
                + sort
                + "&order="
                + order
                + "&help-wanted-issues="
                + help_wanted_issues
                + "&access_token="
                + self.token
                + "?per_page="  # "?simple=yes&per_page="
                + str(self.results_per_page)
                + "&page=1"
            )
            repo_nr_queried = 0
            response = self.session.get(
                search_url, headers=self.headers, timeout=100)
            results = response.json()
            try:
                results_items = results["items"]
            except Exception as err:
                logger.error("Unexpected %s, %s", err, type(err))
                logger.debug("Error raised at data result: %s", results)
                raise
            
            if "last" in response.links:
                nr_of_pages = response.links.get(
                    "last").get("url").split("&page=", 1)[1]
                if results:
                    if int(nr_of_pages) > 1 and repo_nr_queried < repo_nr:
                        repo_nr_queried += self.results_per_page
                        for page in range(2, int(nr_of_pages) + 1):
                            url_repo = (
                                f"{search_url}?simple=yes"
                                f"&per_page=100&page={page}"
                            )
                            res = self.session.get(
                                url_repo, headers=self.headers, timeout=100)
                            logger.info("Query page %s of %s",
                                        page, nr_of_pages)
                            logging.info("Extending results...")
                            try:
                                if "items" in res.json():
                                    next_res = res.json()["items"]
                                    results_items.extend(next_res)
                            except Exception as error:
                                logger.error(
                                    "Could not extend: %s...\nError: %s",
                                    res.json(), error)

            selected_repos = results_items[:repo_nr]
        print(selected_repos)
        self.selected_repos_dict = utils.clean_results(
            selected_repos)

        return selected_repos

    def query_repository(
        self,
        queried_features: List[str],
        filters: Dict[str, Any],
        repo_list: List[int] = []
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Calls functions which perform actual query.
        :param queried_features: List with gathered features
        :return:
        """
        logger.info("Getting request information for feature(s): %s",
                    queried_features)
        feature_list = []  # type: list[str]
        query_dict = {}  # type: dict[str, list]

        if queried_features:
            for feature in queried_features:
                feature_list = (
                    self.query_features[0].get(feature)[0].get("feature_list")
                )
                request_url_1 = (
                    self.query_features[0].get(feature)[0].get("request_url_1")
                )
                request_url_2 = (
                    self.query_features[0].get(feature)[0].get("request_url_2")
                )
                query_dict[feature] = [
                    feature_list, request_url_1, request_url_2]
        request_data_dict = {}
        for param, query in query_dict.items():
            param_list = self.get_repository_data(
                feature_list=query[0],
                request_url_1=query[1],
                request_url_2=query[2],
                filters=filters,
                repo_list=repo_list
            )
            request_data_dict[param] = param_list
        return request_data_dict

    def get_single_object(self,
                          feature: str,
                          filters: Dict[str, Any]
                          ) -> Dict[int,
                                    List[Dict[int,
                                              List[Dict[str,
                                                        Any]]]]]:
        """
        Function to retrieve issues and the comments for each.
        Note: Issues also contain pull requests.
        :param feature: Feature that is to be queried (e.g. commits)
        :return: A dictionary with the repository id,
        its issue ids and the comments per issue.
        """
        request_url_1 = self.query_features[0].get(
            feature)[0].get("request_url_1")
        request_url_2 = self.query_features[0].get(
            feature)[0].get("request_url_2")
        request_url_3 = self.query_features[0].get(
            feature)[0].get("request_url_3")
        logger.info("Starting query for repository request...")
        objects_per_repo = []  # objects_per_repo type: List[Dict[str, Any]]
        objects_per_repo = self.query_repository(
            queried_features=[feature], filters=filters).get(
            feature
        )  # Object e.g. issue or commit
        logger.info("Finished query for repository request.")
        object_key = self.query_features[0].get(feature)[0].get("feature_key")
        single_object_dict = {}
        subfeature_list = self.query_features[0].get(
            feature)[0].get("subfeature_list")
        for repository in objects_per_repo:
            object_list = []
            url = request_url_1 + str(repository) + request_url_2
            objects = objects_per_repo.get(repository)
            object_counter = 0
            for obj in objects:
                object_counter += 1
                logger.info(
                    "Get object Nr. %s of %s", object_counter, len(objects))
                object_id = obj.get(object_key)
                if object_id:
                    comment_dict = utils.get_subfeatures(
                        session=self.session,
                        headers=self.headers,
                        features=subfeature_list,
                        object_id=object_id,
                        object_url=url,
                        sub_url=request_url_3,
                    )
                else:
                    comment_dict = {}
                object_list.append(comment_dict)
            single_object_dict[repository] = object_list
        return single_object_dict

    def get_repository_data(
        self, feature_list: List[str], request_url_1: str,
        request_url_2: str, filters: Dict[str, Any],
        repo_list: List[int]
    ) -> Dict[int, List[Dict[str, Any]]]:
        """
        Query data from repositories
        :param feature_list: Features are the information,
         which should be stored
        after querying to avoid gathering unwanted data.
        :param request_url_1: First part of the url,
        split bc. in some cases
        information such as the repository id must be in the middle of the url.
        :param request_url_2: Second part of the url,
         pointing to the GitHub API subcategory.

        :return: Repository data of the selected features.
        """
        filter_str = ""
        if filters:
            for key, value in filters.items():
                filter_str = filter_str + key + "=" + value + "&"
        logger.info(
            "Getting repository data of %s repositories",
            len(self.selected_repos_dict)
        )
        if repo_list:
            repositories = repo_list
        else:
            repositories = self.selected_repos_dict

        for repo_id in repositories:
            logger.info("Getting repository %s", repo_id)
            if request_url_2:
                url_repo = str(request_url_1 + str(repo_id) + request_url_2)
            else:
                url_repo = str(request_url_1 + str(repo_id))
            logger.info("Getting page 1")
            start_url = (str(url_repo) +
                         "?simple=yes&" +
                         str(filter_str) +
                         "per_page=" +
                         str(self.results_per_page) +
                         "&page=1"
                         )
            response = self.session.get(
                start_url, headers=self.headers, timeout=100)
            results = response.json()

            if "last" in response.links:
                nr_of_pages = (
                    response.links.get("last").get("url").split("&page=", 1)[1]
                )

                if int(nr_of_pages) > 1:
                    logger.info("Getting responses for all pages...")
                    for page in range(2, int(nr_of_pages) + 1):
                        logger.info("Query page %s of %s", page, nr_of_pages)
                        url = (str(url_repo) +
                               "?simple=yes&" +
                               str(filter_str) +
                               "per_page=" +
                               str(self.results_per_page) +
                               "&page=" +
                               str(page))
                        res = self.session.get(
                            url, headers=self.headers, timeout=100)
                        logging.info("Extending results...")
                        try:
                            results.extend(res.json())
                        except Exception as error:
                            logger.info(
                                "Could not extend data: %s:%s",
                                res.json(), error)

            logger.info("Finished getting responses for all queries.")
            element_list = []  # element_list type: List[Dict[str, Any]]
            if isinstance(results, list):
                for element in results:
                    element_dict = {}  # element_dict type: Dict[str, Any]
                    for feature in feature_list:
                        element_dict[feature] = element.get(feature)
                    element_list.append(element_dict)

            elif isinstance(results, dict):
                element_dict = {}  # element_dict type: Dict[str, Any]
                for feature in feature_list:
                    element_dict[feature] = results.get(feature)
                element_list = [element_dict]
            self.repository_dict[repo_id] = element_list
        logger.info("Done getting repository data.")
        return self.repository_dict

    def get_context_information(self, main_feature: str,
                                sub_feature: str, filters: Dict[str, Any]
                                ) -> Dict[int, List[Dict[str, Any]]]:
        """
        :param main_feature: Feature which concerns the main information.
        :param sub_feature: Feature which concerns the context information.
        :return: Dictionary with context information of main feature.
        """
        main_data = self.query_repository([main_feature], filters=filters)
        request_url_1 = self.query_features[0].get(
            sub_feature)[0].get("request_url_1")
        request_url_2 = self.query_features[0].get(
            sub_feature)[0].get("request_url_2")
        feature_list = self.query_features[0].get(
            sub_feature)[0].get("feature_list")
        feature_key = self.query_features[0].get(
            sub_feature)[0].get("feature_key")
        return_data = {}
        for repository, data in main_data.get(main_feature).items():
            data_list = []
            for element in data:
                element_dict = {}
                key = element.get(feature_key)
                element_url = request_url_1 + str(key) + request_url_2
                result = self.session.get(
                            element_url, headers=self.headers, timeout=100)
                sub_data = result.json()
                for feature in feature_list:
                    element_dict[feature] = sub_data.get(feature)
                data_list.append(element_dict)
            return_data[repository] = data_list
        return return_data

#    def __del__(self):
#        self.session.close()

"""
Modle for imports from other sources than GitHub
"""
import requests


def get_osi_json():
    """
    Use licenseId to check for matching entries
    with retrieved data from GitHub to check,
    if license is OSI approved (isOsiApproved)
    """
    url = \
        "https://raw.githubusercontent.com/\
            spdx/license-list-data/master/json/licenses.json"
    response = requests.get(url, timeout=100)
    results_dict = response.json().get("licenses")
    return results_dict


print(get_osi_json()[0])


def get_nvds():
    """
    Placeholder"""
    pass

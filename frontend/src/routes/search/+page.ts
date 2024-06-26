import { PER_PAGE } from '$lib/util';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params, url }) => {
    const term = url.searchParams.get('project')
    const page = url.searchParams.get('page')
    // fetch count of search results from server for pagination
    const response_count = await fetch(`/search/count`, { method: "POST", body: JSON.stringify({ term: term }) });
    let res_count = await response_count.json();

    // fetch search results from server
    const response = await fetch(`/search`, { method: "POST", body: JSON.stringify({ term: term, page: Number(page) <= Math.ceil(res_count['length'] / PER_PAGE) ? page : 1 }) });

    let res;
    if (response.status !== 200) {
        res = [];
    } else {
        res = await response.json();
    }
    return {
        results: res,
        term: term,
        length: res_count['length']
    };
};
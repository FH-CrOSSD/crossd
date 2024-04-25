import type { PageLoad } from './$types';
import { PER_PAGE } from '$lib/util';

export const load: PageLoad = async ({ fetch, params, url }) => {
    const term = url.searchParams.get('project')
    const page = url.searchParams.get('page')
    const response_count = await fetch(`/search/count`, { method: "POST", body: JSON.stringify({ term: term }) });
    let res_count = await response_count.json();

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
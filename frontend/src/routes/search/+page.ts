import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params, url }) => {
    const term = url.searchParams.get('project')
    const response = await fetch(`/search`, { method: "POST", body: JSON.stringify({ term: term }) });
    // console.log(response);
    let res;
    if (response.status !== 200) {
        res = [];
    } else {
        res = await response.json();
    }
    return {
        results: res,
        term: term
    };
};
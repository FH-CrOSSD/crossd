import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params, url }) => {
    const term = url.searchParams.get('project')
    const res = await fetch(`/search`, { method: "POST", body: JSON.stringify({ term: term }) });
    return {
        results: await res.json()
    };
};
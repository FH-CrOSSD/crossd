import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params, url }) => {
    const res = await fetch(`/`, { method: "POST"});
    return {
        results: await res.json()
    };
};
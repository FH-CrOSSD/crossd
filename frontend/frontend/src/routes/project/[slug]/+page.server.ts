import { getMetricsMD } from '$lib/util.server';
import { error } from '@sveltejs/kit';



/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch, params, url }) {
    // const term = url.searchParams.get('project')
    console.log(url);
    const path = url.pathname.split("/");
    // console.log(decodeURIComponent(url.pathname.split("/")[-1]));
    console.log(path);
    console.log(decodeURIComponent(path[path.length - 1]));
    // const res = await fetch(`/search`, { method: "POST", body: JSON.stringify({ term: decodeURIComponent(path[path.length - 1]) }) });
    const res = await fetch(`/metrics/metric`, { method: "POST", body: JSON.stringify({ term: decodeURIComponent(path[path.length - 1]) }) });
    const res2 = await fetch(`/metrics/bak`, { method: "POST", body: JSON.stringify({ term: decodeURIComponent(path[path.length - 1]) }) });
    // console.log(await res.json())
    const data = await res.json();
    const bak = await res2.json();
    const md = await getMetricsMD();
    // return {
    //     results: await res.json()
    // };
    // const post = await getPostFromDatabase(params.slug);
    // do database stuff
    // console.log(data);

    const post = { title: params.slug, data: data, bak: bak, md: md };


    if (post) {
        return post;
    }

    error(404, 'Not found');
}

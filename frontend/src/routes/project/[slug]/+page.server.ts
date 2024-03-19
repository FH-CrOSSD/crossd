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
    const projects_response = await fetch(`/metrics`, { method: "POST", body: JSON.stringify({ term: decodeURIComponent(path[path.length - 1]) }) });
    const projects = (await projects_response.json())[0];
    console.log("new metrics");
    // console.log(await scans.json());
    console.log(projects);
    // console.log((await res_temp.json())[0]['scans'][0]['metric']);


    // const res = await fetch(`/metrics/metric`, { method: "POST", body: JSON.stringify({ term: decodeURIComponent(path[path.length - 1]) }) });
    // const res2 = await fetch(`/metrics/bak`, { method: "POST", body: JSON.stringify({ term: decodeURIComponent(path[path.length - 1]) }) });
    // console.log(await res.json())
    // const data = await res.json();
    // const bak = await res2.json();

    let data: { [key: string]: any } = {};
    let bak: { [key: string]: any } = {};
    let snapshots: { value: string, name: string }[] = [];

    for (let i = 0; i < projects?.scans.length; i++) {
        data[projects.scans[i]['issuedAt']] = projects.scans[i].metric[0];
        bak[projects.scans[i]['issuedAt']] = projects.scans[i].bak[0];
        snapshots.push({ value: projects.scans[i]['issuedAt'].toString(), name: new Date(projects.scans[i]['issuedAt'] * 1000).toUTCString() });

    }

    // console.log(data);
    // console.log(bak);

    const md = await getMetricsMD();
    // return {
    //     results: await res.json()
    // };

    const post = { title: params.slug, data: data, bak: bak, md: md, snapshots: snapshots };


    if (post) {
        return post;
    }

    error(404, 'Not found');
}

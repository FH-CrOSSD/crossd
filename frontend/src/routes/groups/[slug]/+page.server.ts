import { getMetricsMD } from '$lib/util.server';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch, params, url }) {
    const path = url.pathname.split("/");
    // retrieve metrics from /metrics
    const projects_response = await fetch(url, { method: "POST", body: JSON.stringify({ name: decodeURIComponent(params.slug) }) });
    const project = (await projects_response.json());

    // store data retrieved from metrics collections
    // let data: { [key: string]: any } = {};
    // // store data retrieved from bak_metrics collections
    // let bak: { [key: string]: any } = {};
    // // stores timestamp (epoch) and a human-readable interpretation of that timestamp
    // let snapshots: { value: string, name: string }[] = [];

    // for (let i = 0; i < projects?.scans.length; i++) {
    //     data[projects.scans[i]['issuedAt']] = projects.scans[i].metric[0];
    //     bak[projects.scans[i]['issuedAt']] = projects.scans[i].bak[0];
    //     snapshots.push({ value: projects.scans[i]['issuedAt'].toString(), name: new Date(projects.scans[i]['issuedAt'] * 1000).toUTCString() });
    // }

    // metrics mardown for showing the description of a metric on click
    // const md = await getMetricsMD();

    return { name: params.slug, group: project };
}

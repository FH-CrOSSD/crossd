import { getMetricsMD } from '$lib/util.server';

async function getProject(fetch: Function, path: string[]) {
    // retrieve metrics from /metrics
    const projects_response = await fetch(`/metrics`, { method: "POST", body: JSON.stringify({ term: decodeURIComponent(path[path.length - 1]) }) });
    const projects = (await projects_response.json())[0];

    // // store data retrieved from metrics collections
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
    return projects;
}

async function getAvg(fetch: Function) {
    const avg_response = await fetch(`/metrics/avg`, { method: "POST", body: JSON.stringify({}) });
    const avg = (await avg_response.json())["avg"];
    return avg;
}

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch, params, url }) {
    const path = url.pathname.split("/");
    // // retrieve metrics from /metrics
    // const projects_response = await fetch(`/metrics`, { method: "POST", body: JSON.stringify({ term: decodeURIComponent(path[path.length - 1]) }) });
    // const projects = (await projects_response.json())[0];

    // // store data retrieved from metrics collections
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
    const md = await getMetricsMD();
    // const avg_response = await fetch(`/metrics/avg`, { method: "POST", body: JSON.stringify({}) });
    // const avg = (await avg_response.json())["avg"];

    return { title: params.slug, projects: getProject(fetch, path), md: md, avg: getAvg(fetch) };
}

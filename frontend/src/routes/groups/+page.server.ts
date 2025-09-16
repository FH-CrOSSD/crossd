// import { getMetricsMD } from '$lib/util.server';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch, params, url }) {
    // const path = url.pathname.split("/");
    // retrieve metrics from /metrics
    const projects_response = await fetch(`/groups`, { method: "POST" });
    const projects = await projects_response.json();
    return projects
}

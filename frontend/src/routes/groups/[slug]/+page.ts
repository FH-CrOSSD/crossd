async function get_project(url: URL, slug: string) {
    // console.log(url);
    const projects_response = await fetch(url, {
        method: "POST", body: JSON.stringify({ name: decodeURIComponent(slug) }), headers: {
            "Content-Type": "application/json"
        } });
    const project = (await projects_response.json());
    return project;
}
/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch, params, url }) {
    // retrieve metrics from /metrics
    // const projects_response = await fetch(url, { method: "POST", body: JSON.stringify({ name: decodeURIComponent(params.slug) }) });
    // const project = (await projects_response.json());

    // return { name: params.slug, group: project };
    return { name: params.slug, group: get_project(url, params.slug) };
}

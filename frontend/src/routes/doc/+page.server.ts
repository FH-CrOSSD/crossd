import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
// import { readFileSync, readdirSync } from 'fs';
// import path from 'path';
import { getMetricsMD } from '$lib/util.server';
// export const prerender = true;

// const mdpath = path.join("src", "lib", "md");
// const mpath = path.join(mdpath, "metric");
// const mpath = "src/lib/metric_md";
export const load: PageServerLoad = async ({ params }) => {
    // const metrics = readdirSync(mpath);
    // const res: { [key: string]: any } = {};
    // for (let i = 0; i < metrics.length; i++) {
    //     res[metrics[i]] = { text: readFileSync(path.join(mpath, metrics[i]), { encoding: "utf-8" }) };
    // }
    // return { metrics: res, footnotes: { text: readFileSync(path.join(mdpath, "footnotes.md"), { encoding: "utf-8" }) } };
    return getMetricsMD();
};
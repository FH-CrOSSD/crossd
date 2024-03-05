import { readFileSync, readdirSync } from 'fs';
import path from 'path';

const mdpath = path.join("src", "lib", "md");
const mpath = path.join(mdpath, "metric");
export const getMetricsMD = async () => {
    const metrics = readdirSync(mpath);
    const res: { [key: string]: any } = {};
    for (let i = 0; i < metrics.length; i++) {
        res[metrics[i]] = { text: readFileSync(path.join(mpath, metrics[i]), { encoding: "utf-8" }) };
    }
    return { metrics: res, footnotes: { text: readFileSync(path.join(mdpath, "footnotes.md"), { encoding: "utf-8" }) } };
};
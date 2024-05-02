import { getMetricsMD } from '$lib/util.server';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params }) => {
    return getMetricsMD();
};
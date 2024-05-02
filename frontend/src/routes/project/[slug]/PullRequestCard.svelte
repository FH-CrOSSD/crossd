<script lang="ts">
	import { bakGenericDataFn as bgdFn } from '$lib/util';
	import FloatMetricRow from './FloatMetricRow.svelte';
	import MetricCard from './MetricCard.svelte';
	import MetricRow from './MetricRow.svelte';

	export let selected: number;
	export let project_id: string;
	export let data: [{ [key: string]: any }];
	const chart = true;

	let bakGenericDataFn = (category: string, project_id: string, entry: string | null = null) => {
		return bgdFn(category, project_id, entry, data);
	};
</script>

<MetricCard>
	<svelte:fragment slot="heading">Pull requests (PR)</svelte:fragment>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('pull_requests', project_id, 'total_pulls')}
		data_id="a--total-pulls-adopted"
		data_md="change_pull_request">Total PR:</MetricRow
	>
	<FloatMetricRow
		data_id="b--average-pull-closing-time-created"
		data_md="change_pull_request"
		{chart}
		{selected}
		selector={bakGenericDataFn('pull_requests', project_id, 'avg_pull_closing_days')}
		>Average days for closing PR:</FloatMetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('pull_requests', project_id, 'ratio_open_total')}
		data_id="c--open-to-total-pull-requests-ratio-created"
		data_md="change_pull_request">Ratio open PR:</FloatMetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('pull_requests', project_id, 'ratio_closed_total')}
		data_id="d--closed-to-total-pull-requests-ratio-created"
		data_md="change_pull_request">Ratio closed PR:</FloatMetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('pull_requests', project_id, 'ratio_merged_total')}
		data_id="e--merged-to-total-pull-requests-ratio-created"
		data_md="change_pull_request">Ratio merged PR:</FloatMetricRow
	>
</MetricCard>

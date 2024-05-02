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
	<svelte:fragment slot="heading">Issues</svelte:fragment>

	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('issues', project_id, 'total_issues')}
		data_md="issues"
		data_id="e--number-of-total-issues-created">Total issues:</MetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('issues', project_id, 'open_issues')}
		data_md="issues"
		data_id="f--number-of-open-issues-created">Open issues:</MetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('issues', project_id, 'closed_issues')}
		data_md="issues"
		data_id="c--number-of-closed-issues-adopted">Closed issues:</MetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('issues', project_id, 'new_issues')}
		data_md="issues"
		data_id="a--number-of-newcreated-issues-adopted">New issues:</MetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('issues', project_id, 'new_ratio')}
		data_md="issues"
		data_id="b--new-issues-to-total-issues-ratio-adopted">Ratio new issues:</FloatMetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('issues', project_id, 'average_issues_created_per_week')}
		data_md="issues"
		data_id="h--average-issues-created-per-week-created">Average issues created per week:</MetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('issues', project_id, 'average_issue_comments')}
		data_md="issues"
		data_id="i--average-issue-comments-created">Average comments per issue:</MetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('issues', project_id, 'average_issue_resolving_days')}
		data_md="issues"
		data_id="j--average-issue-resolving-days-created">Average days for resolving issues:</MetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('issues', project_id, 'average_first_response_time_days')}
		data_md="issues"
		data_id="k--average-first-response-time-in-days-created"
		>Average days for first response:</MetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('issues', project_id, 'ratio_open_total')}
		data_md="issues"
		data_id="g--open-issues-to-total-issues-ratio-created">Ratio open issues:</FloatMetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('issues', project_id, 'ratio_closed_total')}
		data_md="issues"
		data_id="d--closed-issues-to-total-issues-ratio-adopted">Ratio closed issues:</FloatMetricRow
	>
</MetricCard>

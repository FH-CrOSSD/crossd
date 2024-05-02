<script lang="ts">
	import FloatMetricRow from './FloatMetricRow.svelte';
	import MetricCard from './MetricCard.svelte';
	import MetricRow from './MetricRow.svelte';
	export let selected: number;
	export let project_id: string;
	export let data: [{ [key: string]: any }];
	const chart = true;

	let bakGenericDataFn = (category: string, project_id: string, entry: string | null = null) => {
		return (selected: number) => {
			if (entry) {
				return data[selected]?.[category][project_id][entry] ?? null;
			} else {
				return data[selected]?.[category][project_id] ?? null;
			}
		};
	};
</script>

<MetricCard>
	<svelte:fragment slot="heading">Project velocity</svelte:fragment>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('project_velocity', project_id, 'total_issues')}
		data_md="project_velocity"
		data_id="a--number-of-total-issues-adopted">Total issues:</MetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('project_velocity', project_id, 'closed_issues')}
		data_md="project_velocity"
		data_id="b--number-of-closed-issues-adopted">Closed issues:</MetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('project_velocity', project_id, 'open_issues')}
		data_md="project_velocity"
		data_id="c--number-of-open-issues-created">Open issues:</MetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('project_velocity', project_id, 'pull_count')}
		data_md="project_velocity"
		data_id="d--number-of-total-pull-requests-in-issues-created">Pull count:</MetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('project_velocity', project_id, 'no_pull_count')}
		data_md="project_velocity"
		data_id="e-number-of-total-issues-which-are-no-pull-request-created">No pull count:</MetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('project_velocity', project_id, 'ratio_pull_issue')}
		data_md="project_velocity"
		data_id="f--number-pull-request-to-total-issues-ratio-created">Ratio pull issue:</FloatMetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('project_velocity', project_id, 'avg_issue_resolving_days')}
		data_md="project_velocity"
		data_id="g--average-issue-closing-time-created">Average days for resolving issue:</MetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('project_velocity', project_id, 'ratio_open_total')}
		data_md="project_velocity"
		data_id="h--open-issues-to-total-issues-ratio-created">Ratio open issues:</FloatMetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('project_velocity', project_id, 'ratio_closed_total')}
		data_md="project_velocity"
		data_id="i--closed-issues-to-total-issues-ratio-created">Ratio closed issues:</FloatMetricRow
	>
</MetricCard>

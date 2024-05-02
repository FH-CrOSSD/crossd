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
	<svelte:fragment slot="heading">Lifecycle of branches</svelte:fragment>

	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('branch_lifecycle', project_id, 'branch_creation_frequency_days')}
		data_md="branches"
		data_id="e--branch-creation-frequency-created">Frequency of branch creation (days):</MetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('branch_lifecycle', project_id, 'branch_avg_age_days')}
		data_md="branches"
		data_id="b--average-branch-age-adopted">Average age of branches (days) :</MetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('branch_lifecycle', project_id, 'stale_ratio')}
		data_md="branches"
		data_id="f--stale-branch-to-total-branch-ratio-created">Ratio stale branches:</FloatMetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('branch_lifecycle', project_id, 'active_ratio')}
		data_md="branches"
		data_id="g--active-branch-to-total-branch-ratio-created">Ratio active branches:</FloatMetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('branch_lifecycle', project_id, 'unresolved_ratio')}
		data_md="branches"
		data_id="d--unresolved-branch-to-total-branch-ratio-adapted"
		>Ratio unresolved branches:</FloatMetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('branch_lifecycle', project_id, 'resolved_ratio')}
		data_md="branches"
		data_id="c--resolved-branch-to-total-branch-ratio-adapted"
		>Ratio resolved branches:</FloatMetricRow
	>
</MetricCard>

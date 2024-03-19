<script lang="ts">
	import MetricCard from './MetricCard.svelte';
	import MetricRow from './MetricRow.svelte';
	import FloatMetricRow from './FloatMetricRow.svelte';
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
	<svelte:fragment slot="heading">Distribution of contributions</svelte:fragment>

	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('contributions_distributions', project_id, 'RoF_tail')}
		data_md="contributions_distributions"
		data_id="b--pareto-principle-rof--noc-adopted">Ratio of files tail:</FloatMetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('contributions_distributions', project_id, 'RoF_dominant')}
		data_md="contributions_distributions"
		data_id="b--pareto-principle-rof--noc-adopted">Ratio of files dominant:</FloatMetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('contributions_distributions', project_id, 'RoF_diff_percent')}
		data_md="contributions_distributions"
		data_id="b--pareto-principle-rof--noc-adopted">Ratio of files diff percentage:</FloatMetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn(
			'contributions_distributions',
			project_id,
			'avg_num_contributors_per_file'
		)}
		data_md="contributions_distributions"
		data_id="c--average-contributors-per-file-adapted"
		>Average contributors per file:</FloatMetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('contributions_distributions', project_id, 'bus_factor_score')}
		data_md="contributions_distributions"
		data_id="a--bus-factor-adopted">Bus factor score:</MetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('contributions_distributions', project_id, 'NoC_tail')}
		data_md="contributions_distributions"
		data_id="b--pareto-principle-rof--noc-adopted">Number of commits tail:</FloatMetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('contributions_distributions', project_id, 'NoC_dominant')}
		data_md="contributions_distributions"
		data_id="b--pareto-principle-rof--noc-adopted">Number of commits dominant:</FloatMetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('contributions_distributions', project_id, 'NoC_diff_percent')}
		data_md="contributions_distributions"
		data_id="b--pareto-principle-rof--noc-adopted"
		>Number of commits diff percentage:</FloatMetricRow
	>
</MetricCard>

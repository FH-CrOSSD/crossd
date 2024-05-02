<script lang="ts">
	import { QuestionCircleSolid, ThumbsDownSolid, ThumbsUpSolid } from 'flowbite-svelte-icons';
	import FloatMetricRow from './FloatMetricRow.svelte';
	import IconMetricRow from './IconMetricRow.svelte';
	import MetricCard from './MetricCard.svelte';
	import MetricRow from './MetricRow.svelte';
	export let selected: number;
	export let project_id: string;
	export let data: [{ [key: string]: any }];
	const chart = true;

	let bakGenericDataFn = (category: string, project_id: string, entry: string | null = null) => {
		return (selected: number) => {
			console.log(selected);
			if (entry) {
				return data[selected]?.[category][project_id][entry]??null;
			} else {
				return data[selected]?.[category][project_id]??null;
			}
		};
	};

	function osiIcon(type: string) {
		switch (type) {
			case 'osi_approved':
				return ThumbsUpSolid;
			case 'not_osi_approved':
				return ThumbsDownSolid;
			case 'not_found':
				return QuestionCircleSolid;
		}
	}
</script>

<MetricCard>
	<MetricRow
		data_id="elephant-factor"
		data_md="elephant_factor"
		{selected}
		{chart}
		selector={bakGenericDataFn('elephant_factor', project_id)}>Elephant factor:</MetricRow
	>
	<FloatMetricRow
		data_id="churn"
		data_md="churn"
		{chart}
		{selected}
		selector={bakGenericDataFn('churn', project_id)}>Churn:</FloatMetricRow
	>
	<MetricRow
		data_id="size-of-community"
		data_md="size_of_community"
		{chart}
		{selected}
		selector={bakGenericDataFn('size_of_community', project_id)}>Community size:</MetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('number_of_support_contributors', project_id)}
		data_id="number-of-support-contributors"
		data_md="number_of_support_contributors">Support contributors:</MetricRow
	>
	<FloatMetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('maturity_level', project_id)}
		data_id="maturity-level"
		data_md="maturity_level">Maturity level:</FloatMetricRow
	>
	<IconMetricRow
		data_id="osi-approved-licenses"
		data_md="osi_approved_licenses"
		{selected}
		selector={bakGenericDataFn('osi_approved_license', project_id)}
		iconFn={osiIcon}>OSI approved license:</IconMetricRow
	>
	<FloatMetricRow
		{selected}
		selector={bakGenericDataFn('criticality_score', project_id)}
		{chart}
		data_id="criticality-score"
		data_md="criticality_score">Criticality score:</FloatMetricRow
	>
	<FloatMetricRow
		data_id="support-rate"
		data_md="support_rate"
		{chart}
		{selected}
		selector={bakGenericDataFn('support_rate', project_id)}>Support rate:</FloatMetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('code_dependency', project_id, 'total_upstream')}
		data_id="a--upstream-dependencies-adapted"
		data_md="code_dependencies">Code dependency upstream:</MetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('code_dependency', project_id, 'total_downstream')}
		data_id="b--downstream-dependencies-created"
		data_md="code_dependencies">Code dependency downstream:</MetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('technical_fork', project_id, 'total_forks')}
		data_id="a--total-number-of-created-forks-adopted"
		data_md="technical_fork">Total forks:</MetricRow
	>
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn('technical_fork', project_id, 'average_forks_created_per_week')}
		data_id="b--average-forks-created-per-week-created"
		data_md="technical_fork">Average forks per week:</MetricRow
	>
</MetricCard>

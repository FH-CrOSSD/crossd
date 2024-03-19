<script lang="ts">
	import MetricCard from './MetricCard.svelte';
	import MetricRow from './MetricRow.svelte';
	import FloatMetricRow from './FloatMetricRow.svelte';
	export let selected: number;
	export let project_id: string;
	export let data: [{ [key: string]: any }];
	const chart = true;

	const advisorySelector = (selected: number) => {
		return bakSecurityDataFn('security_advisories', project_id, 'advisories_available')(selected)
			? 'Yes'
			: 'No';
	};

	let bakSecurityDataFn = (category: string, project_id: string, entry: string | null = null) => {
		return (selected: number) => {
			if (entry) {
				return data[selected][category][0][project_id][entry];
			} else {
				return data[selected][category][0][project_id];
			}
		};
	};
</script>

<MetricCard>
	<svelte:fragment slot="heading">Security advisories</svelte:fragment>

	<MetricRow
		{selected}
		selector={advisorySelector}
		data_md="security_advisories"
		data_id="b--existing-advisories-created">Advisories available:</MetricRow
	>
	{#if Object.keys(data[selected]['security_advisories'][0][project_id]).length !== 0}
		<MetricRow
			{chart}
			{selected}
			selector={bakSecurityDataFn('security_advisories', project_id, 'patch_ratio')}
			data_md="security_advisories"
			data_id="c--patched-advisories-to-total-advisories-ratio-created">Ratio patched:</MetricRow
		>
		<MetricRow
			{chart}
			{selected}
			selector={bakSecurityDataFn('security_advisories', project_id, 'closed_advisories')}
			data_md="security_advisories"
			data_id="d--number-of-closed-advisories-created">Number of closed:</MetricRow
		>
		<FloatMetricRow
			{chart}
			{selected}
			selector={bakSecurityDataFn('security_advisories', project_id, 'average_cvss_score')}
			data_md="security_advisories"
			data_id="a--average-cvss-score-adopted">Average CVSS score:</FloatMetricRow
		>
		<FloatMetricRow
			{chart}
			{selected}
			selector={bakSecurityDataFn('security_advisories', project_id, 'ratio_severity_high_crit')}
			data_md="security_advisories"
			data_id="e--advisories-with-critical-or-high-severity-to-total-advisories-ratio-created"
			>Ratio high or critical severity:</FloatMetricRow
		>
	{/if}
</MetricCard>

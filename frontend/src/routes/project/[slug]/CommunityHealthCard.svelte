<script lang="ts">
	import { bakGenericDataFn as bgdFn } from '$lib/util';
	import BoolMetricRow from './BoolMetricRow.svelte';
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
	<svelte:fragment slot="heading">Github community health</svelte:fragment>

	<!-- <MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn(
			'github_community_health_percentage',
			project_id,
			'community_health_score'
		)}
		data_md="github_community_health_percentage"
		data_id="a--github-community-health-percentage-score-adopted">Community Health score:</MetricRow
	> -->
	<MetricRow
		{chart}
		{selected}
		selector={bakGenericDataFn(
			'github_community_health_percentage',
			project_id,
			'custom_health_score'
		)}
		data_md="github_community_health_percentage"
		data_id="b--custom-github-community-health-percentage-score-adapted"
		>Custom Health score:</MetricRow
	>
	<BoolMetricRow
		{selected}
		selector={bakGenericDataFn('github_community_health_percentage', project_id, 'description')}
		data_md="github_community_health_percentage"
		data_id="c--existence-of-single-documents-and-information-created"
		>Has description:</BoolMetricRow
	>
	<!-- <BoolMetricRow
		{selected}
		selector={bakGenericDataFn('github_community_health_percentage', project_id, 'documentation')}
		data_md="github_community_health_percentage"
		data_id="c--existence-of-single-documents-and-information-created"
		>Has documentation:</BoolMetricRow
	> -->
	<BoolMetricRow
		{selected}
		selector={bakGenericDataFn('github_community_health_percentage', project_id, 'code_of_conduct')}
		data_md="github_community_health_percentage"
		data_id="c--existence-of-single-documents-and-information-created"
		>Has code of conduct:</BoolMetricRow
	>
	<BoolMetricRow
		{selected}
		selector={bakGenericDataFn('github_community_health_percentage', project_id, 'contributing')}
		data_md="github_community_health_percentage"
		data_id="c--existence-of-single-documents-and-information-created"
		>Has contributing:</BoolMetricRow
	>
	<BoolMetricRow
		{selected}
		selector={bakGenericDataFn('github_community_health_percentage', project_id, 'issue_template')}
		data_md="github_community_health_percentage"
		data_id="c--existence-of-single-documents-and-information-created"
		>Has issue templates:</BoolMetricRow
	>
	<BoolMetricRow
		{selected}
		selector={bakGenericDataFn(
			'github_community_health_percentage',
			project_id,
			'pull_request_template'
		)}
		data_md="github_community_health_percentage"
		data_id="c--existence-of-single-documents-and-information-created"
		>Has PR templates:</BoolMetricRow
	>
	<BoolMetricRow
		{selected}
		selector={bakGenericDataFn('github_community_health_percentage', project_id, 'license')}
		data_md="github_community_health_percentage"
		data_id="c--existence-of-single-documents-and-information-created">Has license:</BoolMetricRow
	>
	<BoolMetricRow
		{selected}
		selector={bakGenericDataFn('github_community_health_percentage', project_id, 'readme')}
		data_md="github_community_health_percentage"
		data_id="c--existence-of-single-documents-and-information-created">Has README:</BoolMetricRow
	>
	{#if data[selected]?.['version']?.split('.')[0] === '2'}
		<BoolMetricRow
			{selected}
			selector={bakGenericDataFn(
				'github_community_health_percentage',
				project_id,
				'security_policy'
			)}
			data_md="github_community_health_percentage"
			data_id="c--existence-of-single-documents-and-information-created"
			>Has security policy:</BoolMetricRow
		>
	{/if}
</MetricCard>

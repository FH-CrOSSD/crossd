<script lang="ts">
	import { P } from 'flowbite-svelte';
	import { Duration } from 'luxon';
	import BoolMetricRow from './BoolMetricRow.svelte';
	import MetricCard from './MetricCard.svelte';
	import MetricLabel from './MetricLabel.svelte';
	import MetricRow from './MetricRow.svelte';

	export let selected: number;
	export let data: [{ [key: string]: any }];

	let workflow_statuses: { [key: string]: any } = {};
	$: {
		workflow_statuses = {};
		if (data) {
			for (const [key, value] of Object.entries(data[selected]?.current_state_workflows ?? {}) as [
				[string, { [key: string]: any }]
			]) {
				if (!(value['conclusion'] in workflow_statuses)) {
					workflow_statuses[value['conclusion']] = 1;
				} else {
					workflow_statuses[value['conclusion']]++;
				}
			}
		}
	}
	let genericDataFn = (category: string) => {
		return (selected: number) => {
			return data[selected]?.[category] ?? null;
		};
	};

	let dateFn = (category: string) => {
		return (selected: number) => {
			const date = data[selected]?.[category];
			if (typeof date === 'number') {
				return Duration.fromMillis(date)
					.rescale()
					.set({ seconds: 0, milliseconds: 0 })
					.toHuman({ unitDisplay: 'short', showZeros: false });
			} else {
				return date;
			}
		};
	};
</script>

<MetricCard>
	<MetricRow {selected} selector={dateFn('mean_pull_requests')}>Pull Requests (mean):</MetricRow>
	<MetricRow {selected} selector={dateFn('median_pull_requests')}>Pull Requests (median):</MetricRow
	>
	<MetricRow chart={true} {selected} selector={genericDataFn('dependents_count')}
		>Dependents:</MetricRow
	>
	<MetricRow chart={true} {selected} selector={genericDataFn('dependencyCount')}
		>Dependencies:</MetricRow
	>
	<MetricRow chart={true} {selected} selector={genericDataFn('feature_request_count')}
		>Feature Requests:</MetricRow
	>
	<MetricRow chart={true} {selected} selector={genericDataFn('closed_feature_request_count')}
		>Closed Feature Requests:</MetricRow
	>
	<BoolMetricRow {selected} selector={genericDataFn('has_security_policy')}
		>Security Policy:</BoolMetricRow
	>
	<BoolMetricRow {selected} selector={genericDataFn('has_contributing_policy')}
		>Contribution Policy:</BoolMetricRow
	>
	<BoolMetricRow {selected} selector={genericDataFn('has_collaboration_platform')}
		>Collaboration Platform:</BoolMetricRow
	>
	<BoolMetricRow {selected} selector={genericDataFn('is_fundable')}>Fundable:</BoolMetricRow>
	<BoolMetricRow {selected} selector={genericDataFn('uses_workflows')}>Workflows:</BoolMetricRow>
	{#if data[selected]?.['uses_workflows']}
		<MetricLabel>Workflow Statuses:</MetricLabel>
		<P class="max-w-28 break-all wrap-anywhere">
			{#each Object.entries(workflow_statuses) as status}
				{status[1]} {status[0]}<br />
			{/each}
		</P>
	{/if}
</MetricCard>

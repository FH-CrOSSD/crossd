<script lang="ts">
	import { Card, P } from 'flowbite-svelte';
	import MetricLabel from './MetricLabel.svelte';
	import MetricCard from './MetricCard.svelte';
	import Bool from '$lib/Bool.svelte';
	import MetricRow from './MetricRow.svelte';
	import BoolMetricRow from './BoolMetricRow.svelte';
	export let selected: number;
	export let data;
	// export let overlayData;
	// export let overlayData: { content: string; current_id: string; current_text: string };
	export let click: Function;
	// export let workflow_statuses;
	let workflow_statuses: { [key: string]: any } = {};
	$: {
		workflow_statuses = {};
		if (data) {
			for (const [key, value] of Object.entries(data[selected]['current_state_workflows']) as [
				[string, { [key: string]: any }]
			]) {
				if (!(value['conclusion'] in workflow_statuses)) {
					workflow_statuses[value['conclusion']] = 1;
				} else {
					workflow_statuses[value['conclusion']]++;
				}
			}
		}
		// console.log(workflow_statuses);
		// workflow_statuses["failure"]=1;
	}
	let genericDataFn = (category: string) => {
		return (selected: number) => {
			return data[selected][category];

			// console.log(project_id);
		};
	};
</script>

<!-- <MetricRow
	data_id="elephant-factor"
	data_md="elephant_factor"
	bind:selected
	selector={bakGenericDataFn('elephant_factor', project_id, null)}>Elephant factor:</MetricRow
> -->

<MetricCard>
	<MetricRow bind:selected selector={genericDataFn('mean_pull_requests')}
		>Pull Requests (mean):</MetricRow
	>
	<MetricRow bind:selected selector={genericDataFn('median_pull_requests')}
		>Pull Requests (median):</MetricRow
	>
	<MetricRow chart={true} bind:selected selector={genericDataFn('dependents_count')}
		>Dependents:</MetricRow
	>
	<MetricRow chart={true} bind:selected selector={genericDataFn('dependencyCount')}
		>Dependencies:</MetricRow
	>
	<MetricRow chart={true} bind:selected selector={genericDataFn('feature_request_count')}
		>Feature Requests:</MetricRow
	>
	<MetricRow chart={true} bind:selected selector={genericDataFn('closed_feature_request_count')}
		>Closed Feature Requests:</MetricRow
	>
	<BoolMetricRow bind:selected selector={genericDataFn('has_security_policy')}
		>Security Policy:</BoolMetricRow
	>
	<BoolMetricRow bind:selected selector={genericDataFn('has_contributing_policy')}
		>Contribution Policy:</BoolMetricRow
	>
	<BoolMetricRow bind:selected selector={genericDataFn('has_collaboration_platform')}
		>Collaboration Platform:</BoolMetricRow
	>
	<BoolMetricRow bind:selected selector={genericDataFn('is_fundable')}>Fundable:</BoolMetricRow>
	<BoolMetricRow bind:selected selector={genericDataFn('uses_workflows')}>Workflows:</BoolMetricRow>
	{#if data[selected]['uses_workflows']}
		<MetricLabel>Workflow Statuses:</MetricLabel>
		<P class="max-w-xs">
			{#each Object.entries(workflow_statuses) as status}
				{status[1]} {status[0]}<br />
			{/each}
		</P>
	{/if}
	<!-- <MetricLabel {click}>Pull Requests (mean):</MetricLabel>
	<P class="max-w-xs">{data[selected]['mean_pull_requests']}</P> -->
	<!-- <MetricLabel {click}>Pull Requests (median):</MetricLabel>
	<P class="max-w-xs">{data[selected]['median_pull_requests']}</P>
	<MetricLabel {click}>Dependents:</MetricLabel>
	<P class="max-w-xs">{data[selected]['dependents_count']}</P> -->
	<!-- <MetricLabel {click}>Dependencies:</MetricLabel>
	<P class="max-w-xs">{data[selected]['dependencyCount']}</P> -->
	<!-- <MetricLabel {click}>Feature Requests:</MetricLabel>
	<P class="max-w-xs">{data[selected]['feature_request_count']}</P>
	<MetricLabel {click}>Closed Feature Requests:</MetricLabel>
	<P class="max-w-xs">{data[selected]['closed_feature_request_count']}</P> -->
	<!-- <MetricLabel {click}>Security Policy:</MetricLabel> -->
	<!-- <P class="max-w-xs"><Bool value={data[selected]['has_security_policy']} /></P> -->
	<!-- <MetricLabel {click}>Contribution Policy:</MetricLabel>
	<P class="max-w-xs"><Bool value={data[selected]['has_contributing_policy']} /></P>
	<MetricLabel {click}>Collaboration Platform:</MetricLabel>
	<P class="max-w-xs"><Bool value={data[selected]['has_collaboration_platform']} /></P> -->
	<!-- <MetricLabel {click}>Fundable:</MetricLabel>
	<P class="max-w-xs"><Bool value={data[selected]['is_fundable']} /></P>
	<MetricLabel {click}>Workflows:</MetricLabel>
	<P class="max-w-xs"><Bool value={data[selected]['uses_workflows']} /></P> -->
	<!-- {#if data[selected]['uses_workflows']}
		<MetricLabel {click}>Workflow Statuses:</MetricLabel>
		<P class="max-w-xs">
			{#each Object.entries(workflow_statuses) as status}
				{status[1]} {status[0]}<br />
			{/each}
		</P>
	{/if} -->
</MetricCard>

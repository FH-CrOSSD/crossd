<script lang="ts">
	import MetricCard from './MetricCard.svelte';
	import MetricRow from './MetricRow.svelte';
	import { bakGenericDataFn as bgdFn, toFixed2 } from '$lib/util';
	import { Heading, Listgroup, Tooltip } from 'flowbite-svelte';
	import FloatMetricRow from './FloatMetricRow.svelte';
	import MetricValue from './MetricValue.svelte';
	import { chartOptions } from '$lib/chartOptions';
	import { clickedSelector, overlayStore } from './Row.svelte';
	import { Chart } from '@flowbite-svelte-plugins/chart';

	let { data, selected, avg, project_id = null, snapshots } = $props();

	let chartOpts = $state(chartOptions);

	function prepareChart(name: string) {
		// Get HTML element of selected metric
		// const elem = document.querySelector('[data-id="' + id + '"]');
		// use name as title for the chart
		// console.log(snapshots);
		chartOpts.series[0].name = name;
		// prepare the data for the chart - get the value of the metric for the snapshot, format them and filter empty values
		chartOpts.series[0].data = snapshots
			.map((x) => {
				let val = selector(x.value);
				return val % 1 === 0 ? val : toFixed2(val);
			})
			.filter((item) => !(item === undefined || item === null));
		// prepare the ticks for the x axis - filter empty values and format the dates into a nice format in UTC time
		chartOpts.xaxis.categories = snapshots
			.filter((item) => {
				let val = selector(item.value);
				return !(val === undefined || val === null);
			})
			.map((x) => {
				return new Date(Date.parse(x.name)).toLocaleString('eo');
			});
		// return {...chartOpts};
	}
	let bakGenericDataFn = (
		category: string,
		project_id: string | null,
		entry: string | null = null
	) => {
		return bgdFn(category, project_id, entry, data);
	};
	let genericDataFn = (category: string) => {
		return (selected: number) => {
			return data[selected]?.[category] ?? null;
		};
	};
	function prepareSelector(id: string) {
		switch (id) {
			case 'elephant_factor':
			case 'maturity_level':
			case 'criticality_score':
			case 'support_rate':
				selector = bakGenericDataFn(id, project_id);
				break;
			case 'github_community_health_percentage':
				selector = bakGenericDataFn(id, project_id, 'custom_health_score');
				break;
		}
	}
	let selector = bakGenericDataFn('elephant_factor', project_id);
	function isWithinRange(value: number, reference: number, threshold: number = 0.1) {
		return Math.abs(value - reference) <= reference * threshold;
	}
	function isWithinRangePos(value: number, reference: number, threshold: number = 0.1) {
		// console.log(value);
		// console.log(reference);
		// console.log(threshold);
		return value > reference || Math.abs(value - reference) <= reference * threshold;
	}

	function getColorClasses(value: number, reference: number) {
		// console.log(reference);
		if (isWithinRangePos(value, reference, 0.15)) {
			return 'dark:text-emerald-400 text-emerald-500';
		} else if (isWithinRangePos(value, reference, 0.25)) {
			return 'dark:text-amber-400 text-amber-500';
		} else {
			return 'dark:text-rose-400 text-rose-500';
		}
	}
	prepareChart('Elephant factor');

	let buttonsTemplate = [
		{ name: 'Elephant factor', data: 'elephant_factor' },
		{ name: 'Maturity level', data: 'maturity_level' },
		{ name: 'Criticality score', data: 'criticality_score' },
		{ name: 'Support rate', data: 'support_rate' },
		{ name: 'Github community health percentage', data: 'github_community_health_percentage' }
	];
	let currentButton = $state('Elephant factor');
	let buttons = $derived.by(() => {
		// console.log(currentButton);
		let c = [];
		for (const elem of buttonsTemplate) {
			// console.log(elem);
			let tmp = { ...elem };
			if (tmp.name == currentButton) {
				tmp.current = true;
			} else {
				tmp.current = false;
			}
			c.push(tmp);
		}
		return c;
	});
	async function chartClick(e) {
		currentButton = e?.detail['name'];
		prepareSelector(e?.detail['data']);
		prepareChart(e?.detail['name']);
		// console.log(chartOpts);
	}
</script>

<div class="flex gap-10">
	<MetricCard>
		<Heading tag="h4">Stats</Heading>
		<div></div>
		<MetricRow
			{selected}
			selector={bakGenericDataFn('elephant_factor', project_id)}
			valueClass={getColorClasses(
				bakGenericDataFn('elephant_factor', project_id)(selected),
				avg.elephant_factor
			)}>Elephant factor:</MetricRow
		>
		<Tooltip color="gray">Average: {avg.elephant_factor}</Tooltip>
		<FloatMetricRow
			{selected}
			selector={bakGenericDataFn('maturity_level', project_id)}
			valueClass={getColorClasses(
				bakGenericDataFn('maturity_level', project_id)(selected),
				avg.maturity_level
			)}>Maturity level:</FloatMetricRow
		>
		<Tooltip color="gray">Average: {avg.maturity_level}</Tooltip>
		<FloatMetricRow
			{selected}
			selector={bakGenericDataFn('criticality_score', project_id)}
			valueClass={getColorClasses(
				bakGenericDataFn('criticality_score', project_id)(selected),
				avg.criticality_score
			)}>Criticality score:</FloatMetricRow
		>
		<Tooltip color="gray">Average: {avg.criticality_score}</Tooltip>
		<FloatMetricRow
			{selected}
			selector={bakGenericDataFn('support_rate', project_id)}
			valueClass={getColorClasses(
				bakGenericDataFn('support_rate', project_id)(selected),
				avg.support_rate
			)}>Support rate:</FloatMetricRow
		>
		<Tooltip color="gray">Average: {avg.support_rate}</Tooltip>
		<FloatMetricRow
			{selected}
			selector={bakGenericDataFn(
				'github_community_health_percentage',
				project_id,
				'custom_health_score'
			)}
			valueClass={getColorClasses(
				bakGenericDataFn(
					'github_community_health_percentage',
					project_id,
					'custom_health_score'
				)(selected),
				avg.github_community_health_percentage
			)}>Github community healh:</FloatMetricRow
		>
		<Tooltip color="gray">Average: {avg.github_community_health_percentage}</Tooltip>
	</MetricCard>

	<div
		class="flex gap-5 p-5 border border-solid border-gray-200 dark:border-gray-700 shadow-md rounded-md"
	>
		<!-- <Chart options={chartOptions} size="lg" /> -->
		<div class="chart-container ml-10">
			<Chart options={chartOpts} class="w-fill min-w-96" />
		</div>
		<Listgroup
			id="lgroup1"
			active
			items={buttons}
			class="w-50"
			onclick={chartClick}
			itemClass="h-1/5"
		></Listgroup>
	</div>
</div>

<style>
	:global(#lgroup1 > button[aria-current='true']) {
		background-color: light-dark(#f3f4f6, #101828);
		color: #ef562f;
		/* #26a0fc */
	}
</style>

<script lang="ts">
	import MetricCard from './MetricCard.svelte';
	import MetricRow from './MetricRow.svelte';
	import { bakGenericDataFn as bgdFn, toFixed2 } from '$lib/util';
	import { Alert, Heading, Indicator, Listgroup, P, Tooltip } from 'flowbite-svelte';
	import FloatMetricRow from './FloatMetricRow.svelte';
	import MetricValue from './MetricValue.svelte';
	import { chartOptions } from '$lib/chartOptions';
	import { clickedSelector, overlayStore } from './Row.svelte';
	import { Chart } from '@flowbite-svelte-plugins/chart';
	import { ExclamationCircleOutline } from 'flowbite-svelte-icons';

	let { data, ai, selected, project_id = null, snapshots } = $props();

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
	let val = (key:string, value:string) => {
		return (selected: number) => {
			return ai[selected]["result"]?.[key]?.[value] ?? null;
		};
	};
</script>
<Alert color="amber" class="mb-4 py-2">
{#snippet icon()}<ExclamationCircleOutline class="h-5 w-5" />{/snippet}
	These metrics are generated using artificial intelligence operating on repository data and may contain errors or inaccuracies.
	<br>We do not guarantee its completeness or reliability.
</Alert>
<div class="flex flex-wrap gap-10">
	<!-- {JSON.stringify(ai,null,4)} -->
	<MetricCard cardClass="min-w-[48%]">
		<svelte:fragment slot="heading">{ai[selected]["result"]["friendliness"]["display_name"]}</svelte:fragment>
		<MetricRow bind:selected selector={val("friendliness","metric")}>Metric:</MetricRow>
		<br>
		<!-- <MetricRow bind:selected selector={val("friendliness","explanation")}>Explanation:</MetricRow> -->
		<svelte:fragment slot="remainder"><P>Explanation:</P><P><br>{ai[selected]["result"]["friendliness"]["explanation"]}</P></svelte:fragment>
	</MetricCard>
	<MetricCard cardClass="min-w-[48%]">
		<svelte:fragment slot="heading">{ai[selected]["result"]["documentation_quality"]["display_name"]}</svelte:fragment>
		<MetricRow bind:selected selector={val("documentation_quality","metric")}>Metric:</MetricRow>
		<br>
		<!-- <MetricRow bind:selected selector={val("documentation_quality","explanation")}>Explanation:</MetricRow> -->
		<svelte:fragment slot="remainder"><P>Explanation:</P><P><br>{ai[selected]["result"]["documentation_quality"]["explanation"]}</P></svelte:fragment>
	</MetricCard>
	<MetricCard cardClass="min-w-[48%]">
		<svelte:fragment slot="heading">{ai[selected]["result"]["development_efficiency"]["display_name"]}</svelte:fragment>
		<MetricRow bind:selected selector={val("development_efficiency","metric")}>Metric:</MetricRow>
		<br>
		<!-- <MetricRow bind:selected selector={val("development_efficiency","explanation")}>Explanation:</MetricRow> -->
		<svelte:fragment slot="remainder"><P>Explanation:</P><P><br>{ai[selected]["result"]["development_efficiency"]["explanation"]}</P></svelte:fragment>
	</MetricCard>
	<MetricCard cardClass="min-w-[48%]">
		<svelte:fragment slot="heading">{ai[selected]["result"]["project_maturity"]["display_name"]}</svelte:fragment>
		<MetricRow bind:selected selector={val("project_maturity","metric")}>Metric:</MetricRow>
		<FloatMetricRow
			{selected}
			selector={bakGenericDataFn('maturity_level', project_id)}
			>Maturity level: <br> <span class="text-amber-600">(non-AI metric)</span></FloatMetricRow
		>
		<br>
		<!-- <MetricRow bind:selected selector={val("project_maturity","explanation")}>Explanation:</MetricRow> -->
		<svelte:fragment slot="remainder"><P>Explanation:</P><P><br>{ai[selected]["result"]["project_maturity"]["explanation"]}</P></svelte:fragment>
	</MetricCard>
	<!-- <MetricCard>
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
		{#snippet remainder()}
			<div class="flex mt-auto text-gray-500 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 border-l-4 border-gray-300 dark:border-gray-500 px-2 text-sm rounded">
			<span class="mr-auto">&lt; than avg:</span>
			<span class="flex items-center">
				<Indicator size="sm" class="dark:bg-emerald-400 bg-emerald-500 me-1.5" />&lt;= 15%
			</span>
			<span class="flex items-center ml-2">
				<Indicator size="sm" class="dark:bg-amber-400 bg-amber-500 me-1.5" />&lt;= 25%
			</span>
			<span class="flex items-center ml-2">
				<Indicator size="sm" class="dark:bg-rose-400 bg-rose-500 me-1.5" />&gt; 25%
			</span>
		</div>
		{/snippet}
		
	</MetricCard> -->
<!-- 
	<div
		class="flex gap-5 p-5 border border-solid border-gray-200 dark:border-gray-700 shadow-md rounded-md"
	>
		<div class="chart-container ml-10">
			<Chart options={chartOpts} class="w-fill min-w-96" />
		</div>
		<Listgroup
			id="lgroup1"
			active
			items={buttons}
			class="w-50"
			onclick={chartClick}
			itemClass='h-1/5 cursor-pointer aria-[current=true]:bg-[#f3f4f6] aria-[current=true]:dark:bg-[#101828] aria-[current=true]:text-[#ef562f] aria-[current=true]:dark:text-[#ef562f]'
			></Listgroup>
	</div> -->
</div>


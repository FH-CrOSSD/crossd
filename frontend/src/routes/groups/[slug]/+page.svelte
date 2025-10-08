<script lang="ts">
	import { chartOptions } from '$lib/chartOptions';
	import { Chart } from '@flowbite-svelte-plugins/chart';
	import {
		A,
		Badge,
		Card,
		CardPlaceholder,
		Heading,
		Hr,
		P,
		Skeleton,
		WidgetPlaceholder
	} from 'flowbite-svelte';
	import {
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
		TableSearch,
		Tabs,
		TabItem
	} from 'flowbite-svelte';

	/** @type {import('./$types').PageData */
	/** @type {import('./$types').PageData */
	// export let data: {
	// 	name: string;
	// 	group: [{ [key: string]: any }];
	// };
	import type { PageProps } from './$types';
	import LoadingStatistics from './LoadingStatistics.svelte';
	import Statistics from './Statistics.svelte';
	import { page } from '$app/state';
	import { Listgroup } from 'flowbite-svelte';
	let buttonsTemplate = [
		{ name: 'Elephant factor', data: 'elephant_factor' },
		{ name: 'Maturity level', data: 'maturity_level' },
		{ name: 'Criticality score', data: 'criticality_score' },
		{ name: 'Support rate', data: 'support_rate' },
		{ name: 'Github community health percentage', data: 'github_community_health_percentage.custom_health_score' }
	];
	let currentButton = $state('Elephant factor');
	let buttons = $derived.by(() => {
		console.log(currentButton);
		let c = [];
		for (const elem of buttonsTemplate) {
			console.log(elem);
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

	let { data }: PageProps = $props();
	let test = $state();
	data.group.then((val) => (test = val));

	let chart = $state();
	data.chart.then((val) => (chart = val));
	let searchTerm = $state('');
	let filteredItems = $derived.by(() => {
		return test?.projects?.filter(
			(item) => !searchTerm || item.toLowerCase().includes(searchTerm.toLowerCase())
		);
	});
	let activeTab = $state('avg');
	let activeClass =
		'inline-block text-sm font-medium text-center disabled:cursor-not-allowed active p-4 text-primary-600 bg-gray-100 rounded-t-lg dark:bg-gray-900 dark:text-primary-500';

	// chartOptions.yaxis['labels']["style"] =  {
	//             fontFamily: 'Inter, sans-serif',
	//             cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400'
	//         };

	let chartOpts = $derived.by(() => {
		if (chart) {
			console.log('doStuff');
			let opts = { ...chartOptions };
			let x: [] = [];
			let y: [] = [];
			for (const elem of chart) {
				x.push(elem[activeTab]);
				y.push(elem['month']);
			}

			opts.series[0].data = x;
			opts.xaxis.categories = y;
			opts.chart.type = 'bar';
			opts.yaxis['labels'] = {
				minWidth: 35,
				offsetY: 1,
				style: {
					fontFamily: 'Inter, sans-serif',
					cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400'
				}
			};
			console.log(opts);
			return opts;
		}
	});
	async function chartClick(e) {
		currentButton = e?.detail['name'];
		const res = await fetch(page.url + '/chart', {
			method: 'POST',
			body: JSON.stringify({
				name: decodeURIComponent(page.params.slug),
				parameter: e?.detail['data']
			}),
			headers: {
				'Content-Type': 'application/json'
			}
		});
		const jres = await res.json();
		console.log(jres);
		chart = jres;
		console.log(chart);
	}
	// let chartelem=new Chart(chartOpts);
	// $: filteredItems = data.group.projects?.filter(
	// 	(item) => !searchTerm || item.toLowerCase().includes(searchTerm.toLowerCase())
	// );
</script>

<div class="flex">
	<div class="w-full pr-8">
		<Heading tag="h1" class="mb-4"
			>Group <span class="bg-gray-200 dark:bg-gray-600 px-1 rounded-md">{data.name}</span></Heading
		>
		{#await data.group}
			<LoadingStatistics />
		{:then group}
			<!-- <Statistics name={data.name} count={test?.projects?.length} elephant_factor={group.data.elephant_factor} maturity_level={group.data.maturity_level}/> -->
			<Tabs style="underline" class="w-full" classes={{ content: 'bg-white dark:bg-gray-800' }}>
				<TabItem
					open
					title="Avg"
					{activeClass}
					onclick={() => {
						activeTab = 'avg';
					}}
				>
					<div class="flex gap-10">
						<Statistics
							{...{
								name: data.name,
								count: test?.projects?.length,
								elephant_factor: group.data.avg.elephant_factor,
								maturity_level: group.data.avg.maturity_level,
								criticality_score: group.data.avg.criticality_score,
								support_rate: group.data.avg.support_rate,
								github_community_health_percentage:
									group.data.avg.github_community_health_percentage
							}}
						/>
						{#await data.chart}
							<WidgetPlaceholder />
						{:then dchart}
							<div
								class="flex gap-5 p-5 border border-solid border-gray-200 dark:border-gray-700 shadow-md rounded-md"
							>
								<Chart bind:options={chartOpts} class="w-fill min-w-96" />
								<Listgroup
									id="lgroup1"
									active
									items={buttons}
									class="w-50"
									onclick={chartClick}
									itemClass="h-1/5 cursor-pointer"
								></Listgroup>
							</div>
						{/await}
					</div>
				</TabItem>
				<TabItem
					title="Min"
					{activeClass}
					onclick={() => {
						activeTab = 'min';
					}}
				>
					<div class="flex gap-10">
						<Statistics
							{...{
								name: data.name,
								count: test?.projects?.length,
								elephant_factor: group.data.min.elephant_factor,
								maturity_level: group.data.min.maturity_level,
								criticality_score: group.data.min.criticality_score,
								support_rate: group.data.min.support_rate,
								github_community_health_percentage:
									group.data.min.github_community_health_percentage
							}}
						/>
						{#await data.chart}
							<WidgetPlaceholder />
						{:then dchart}
							<div
								class="flex gap-5 p-5 border border-solid border-gray-200 dark:border-gray-700 shadow-md rounded-md"
							>
								<Chart options={chartOpts} class="w-fill min-w-96" />
								<Listgroup
									id="lgroup1"
									active
									items={buttons}
									class="w-50"
									onclick={chartClick}
									itemClass="h-1/5 cursor-pointer"
								></Listgroup>
							</div>
						{/await}
					</div>
				</TabItem>
				<TabItem
					title="Max"
					{activeClass}
					onclick={() => {
						activeTab = 'max';
					}}
				>
					<div class="flex gap-10">
						<Statistics
							{...{
								name: data.name,
								count: test?.projects?.length,
								elephant_factor: group.data.max.elephant_factor,
								maturity_level: group.data.max.maturity_level,
								criticality_score: group.data.max.criticality_score,
								support_rate: group.data.max.support_rate,
								github_community_health_percentage:
									group.data.max.github_community_health_percentage
							}}
						/>
						{#await data.chart}
							<WidgetPlaceholder />
						{:then dchart}
							<div
								class="flex gap-5 p-5 border border-solid border-gray-200 dark:border-gray-700 shadow-md rounded-md"
							>
								<Chart options={chartOpts} class="w-fill min-w-96" />
								<Listgroup
									id="lgroup1"
									active
									items={buttons}
									class="w-50"
									onclick={chartClick}
									itemClass="h-1/5 cursor-pointer"
								></Listgroup>
							</div>
						{/await}
					</div>
				</TabItem>
				<TabItem
					title="Agg"
					{activeClass}
					onclick={() => {
						activeTab = 'agg';
					}}
				>
					<div class="flex gap-10">
						<Statistics
							{...{
								name: data.name,
								count: test?.projects?.length,
								elephant_factor: group.data.sum.elephant_factor,
								maturity_level: group.data.sum.maturity_level,
								criticality_score: group.data.sum.criticality_score,
								support_rate: group.data.sum.support_rate,
								github_community_health_percentage:
									group.data.sum.github_community_health_percentage
							}}
						/>{#await data.chart}
							<WidgetPlaceholder />
						{:then dchart}
							<div
								class="flex gap-5 p-5 border border-solid border-gray-200 dark:border-gray-700 shadow-md rounded-md"
							>
								<Chart options={chartOpts} class="w-fill min-w-96" />
								<Listgroup
									id="lgroup1"
									active
									items={buttons}
									class="w-50"
									onclick={chartClick}
									itemClass="h-1/5 cursor-pointer"
								></Listgroup>
							</div>
						{/await}
					</div>
				</TabItem>

				<TabItem
					title="Stddev"
					{activeClass}
					onclick={() => {
						activeTab = 'stddev';
					}}
				>
					<div class="flex gap-10">
						<Statistics
							{...{
								name: data.name,
								count: test?.projects?.length,
								elephant_factor: group.data.stddev.elephant_factor,
								maturity_level: group.data.stddev.maturity_level,
								criticality_score: group.data.stddev.criticality_score,
								support_rate: group.data.stddev.support_rate,
								github_community_health_percentage:
									group.data.stddev.github_community_health_percentage
							}}
						/>
						{#await data.chart}
							<WidgetPlaceholder />
						{:then dchart}
							<div
								class="flex gap-5 p-5 border border-solid border-gray-200 dark:border-gray-700 shadow-md rounded-md"
							>
								<Chart options={chartOpts} class="w-fill min-w-96" />
								<Listgroup
									id="lgroup1"
									active
									items={buttons}
									class="w-50"
									onclick={chartClick}
									itemClass="h-1/5 cursor-pointer"
								></Listgroup>
							</div>
						{/await}
					</div>
				</TabItem>
			</Tabs>
		{/await}
	</div>

	<div class="w-1/3 ml-auto h-[calc(65vh))] sticky top-10">
		<Heading tag="h4" class="mx-5 mt-5">Group repositories</Heading>
		<TableSearch
			placeholder="Search by name"
			hoverable
			bind:inputValue={searchTerm}
			divClass="shadow-none overflow-y-visible h-full scrollbar"
			tableClass=""
			searchClass="pr-2"
			striped={true}
		>
			<!-- <Table shadow={false} border={false}> -->
			<TableHead class="">
				<TableHeadCell class="flex"
					><P>Repository</P><Badge color="sky" class="block ml-auto w-fit"
						>{filteredItems?.length || 0}</Badge
					></TableHeadCell
				>
			</TableHead>
			<TableBody class="">
				{#await data.group}
					<TableBodyRow>
						<TableBodyCell><Skeleton></Skeleton></TableBodyCell>
					</TableBodyRow>
				{:then group}
					{#each filteredItems as item}
						<TableBodyRow>
							<A class="w-full wrap-anywhere" href="/project/{encodeURIComponent(item)}">
								<TableBodyCell class="whitespace-normal">{item}</TableBodyCell>
							</A>
						</TableBodyRow>
					{/each}
				{/await}
			</TableBody>
			<!-- </Table> -->
		</TableSearch>
	</div>
</div>

<style>
	:global(.scrollbar) {
		overflow: auto;
		scrollbar-width: thin;
		scrollbar-color: light-dark(black, white) light-dark(lightslategray, darkslategray);
	}
	:global(#lgroup1 > button[aria-current='true']) {
		background-color: light-dark(#f3f4f6, #101828);
		color: #ef562f;
		/* #26a0fc */
	}
</style>

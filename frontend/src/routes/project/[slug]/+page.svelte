<script lang="ts">
	import { chartOptions } from '$lib/chartOptions';
	import { processMD, toFixed2 } from '$lib/util';
	import {
		A,
		Card,
		CardPlaceholder,
		CloseButton,
		Drawer,
		Drawerhead,
		Heading,
		Hr,
		Modal,
		P,
		Select,
		Skeleton,
		TabItem,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
		Tabs,
		WidgetPlaceholder
	} from 'flowbite-svelte';
	import { Chart } from '@flowbite-svelte-plugins/chart';
	import { onDestroy } from 'svelte';
	import { sineIn } from 'svelte/easing';
	import CommunityHealthCard from './CommunityHealthCard.svelte';
	import DistributionContributionCard from './DistributionContributionCard.svelte';
	import GenericBakCard from './GenericBakCard.svelte';
	import GenericMetricCard from './GenericMetricCard.svelte';
	import IssueCard from './IssueCard.svelte';
	import LifecycleBranchesCard from './LifecycleBranchesCard.svelte';
	import ProjectVelocityCard from './ProjectVelocityCard.svelte';
	import PullRequestCard from './PullRequestCard.svelte';
	import { clickedSelector, overlayStore } from './Row.svelte';
	import SecurityAdvisoriesCard from './SecurityAdvisoriesCard.svelte';
	import { draw } from 'svelte/transition';
	import Details from './Details.svelte';
	import Overview from './Overview.svelte';
	import { GithubSolid } from 'flowbite-svelte-icons';

	/** @type {import('./$types').PageData */
	export let data: {
		title: string;
		data: [{ [key: string]: any }];
		bak: [{ [key: string]: any }];
		md: [{ [key: string]: any }];
		avg: { [key: string]: any };
	};

	let project_id: string;
	let snapshots: Array<{ value: number; name: string }>;
	let selected: string;
	let overlayID: string;
	let showChart: boolean = false;
	let showDefinition: boolean = false;
	let overlayMD: string;
	let scrollFinished = false;
	let drawerHidden = false;
	// store data retrieved from metrics collections
	let projects = {};
	let projectData: { [key: string]: any } = {};
	// store data retrieved from bak_metrics collections
	let bak: { [key: string]: any } = {};
	let avg;
	// stores timestamp (epoch) and a human-readable interpretation of that timestamp
	chartOptions.chart.type = 'line';
	// hide drawer if there is no definition to show or if the chart should not be shown
	$: {
		drawerHidden = showDefinition === true ? showChart : false;
		// drawerHidden;
		// console.log(showDefinition);
		// console.log(drawerHidden);
	}
	// transition for the drawer (sidebar)
	// const transitionParamsRight = {
	// 	x: 320,
	// 	duration: 200,
	// 	easing: sineIn
	// };

	data.projects.then((val) => {
		projects = val;
	});

	data.avg.then((val) => {
		avg = val;
	});

	$: {
		if (projects?.scans) {
			let tmpdata = {};
			let tmpbak = {};
			let tmpsnapshots = [];

			for (let i = 0; i < projects?.scans.length; i++) {
				tmpdata[projects.scans[i]['issuedAt']] = projects.scans[i].metric[0];
				tmpbak[projects.scans[i]['issuedAt']] = projects.scans[i].bak[0];
				if (Object.keys(projects.scans[i].metric[0] ?? {}).length > 0 || projects.scans[i].bak[0]) {
					tmpsnapshots.push({
						value: projects.scans[i]['issuedAt'].toString(),
						name: new Date(projects.scans[i]['issuedAt'] * 1000).toUTCString()
					});
				}
			}
			projectData = tmpdata;
			bak = tmpbak;
			snapshots = tmpsnapshots;
			updateSelected();
		}
	}

	// components can trigger the drawer by setting a value in the store
	let unsubscribe = overlayStore.subscribe((value) => {
		if (value) {
			showChart = value.chart;
			showDefinition = value.definition;
			if (value.definition === true) {
				// prepare for the metric definition, render markdown
				overlayID = value.current_id;
				goToDefinition(value.current_md);
			}
			if (value.chart === true) {
				prepareChart(value.current_id);
			}
			// reset the store
			$overlayStore = null;
		}
	});

	// set the selected snapshot when data is modified
	function updateSelected() {
		selected = snapshots && snapshots.length > 0 ? snapshots[snapshots.length - 1]['value'] : 0;
	}

	// render markdown, show sidebar
	async function goToDefinition(md: string) {
		overlayMD = (
			await processMD(
				data.md['metrics'][md + '.md']['text'] + '\n\n' + data.md['footnotes']['text']
			)
		).toString();
		drawerHidden = true;
	}

	function prepareChart(id: string) {
		// Get HTML element of selected metric
		const elem = document.querySelector('[data-id="' + id + '"]');
		// use name as title for the chart
		chartOptions.series[0].name = elem ? elem.innerText : 'Data:';
		// prepare the data for the chart - get the value of the metric for the snapshot, format them and filter empty values
		chartOptions.series[0].data = snapshots
			.map((x) => {
				let val = $clickedSelector(x.value);
				return val % 1 === 0 ? val : toFixed2(val);
			})
			.filter((item) => !(item === undefined || item === null));
		// prepare the ticks for the x axis - filter empty values and format the dates into a nice format in UTC time
		chartOptions.xaxis.categories = snapshots
			.filter((item) => {
				let val = $clickedSelector(item.value);
				return !(val === undefined || val === null);
			})
			.map((x) => {
				return new Date(Date.parse(x.name)).toLocaleString('eo');
			});
	}

	// scroll to a specific metric documentation element
	async function scroll() {
		document.getElementById(overlayID).scrollIntoView();
		scrollFinished = true;
	}

	// scroll to a specific element when the drawer is shown
	/** @type {import('svelte/action').Action}  */
	function onShown(node) {
		// the node has been mounted in the DOM
		const observer = new IntersectionObserver((entries) => {
			if (entries.some((x) => x.isIntersecting)) {
				// element in viewport
				if (!scrollFinished) {
					scroll();
				}
			}
		}, {});

		observer.observe(node);
		return {
			destroy() {
				observer.disconnect();
				console.log('destroyed');
				scrollFinished = false;
				// the node has been removed from the DOM
			}
		};
	}

	// whenever data changes
	// $: {
	// 	snapshots = data.snapshots;
	// 	updateSelected();
	// }

	// whener bak changes
	// retrieve the project id, which is used in all bak metrics
	// elephant_factor is always there, so we chose it to retrieve the project id
	$: {
		if (bak) {
			project_id = Object.keys(bak[selected]?.elephant_factor ?? [])[0];
		}
	}

	// unsubscribe from the overlayStore when user leaves the page
	onDestroy(() => {
		console.log('the component is being destroyed');
		unsubscribe();
	});
</script>

<div class="flex gap-10">
	<div class="w-4/5">
		{#await Promise.all([data.projects, data.avg])}
			<Heading class="flex break-words max-w-[calc(100%-25rem)]" tag="h1">{data.title} <A
						class="text-black dark:text-white hover:text-primary-500 dark:hover:text-primary-500"
						href="https://github.com/{data.title}"><GithubSolid class="ml-2 h-full w-10" /></A
					></Heading>
			<Hr />
			<Tabs style="underline" class="w-full" classes={{ content: 'bg-white dark:bg-gray-800' }}>
				<TabItem open class="">
					{#snippet titleSlot()}
						<div
							class="mb-2.5 h-2.5 w-32 rounded-full bg-gray-200 dark:bg-gray-700 animate-pulse"
						></div>
					{/snippet}
					<div class="flex flex-wrap gap-10">
						<Card class="p-5">
							<Heading tag="h4" class="mb-5">Stats</Heading>
							<Skeleton size="sm" class="my-5"></Skeleton>
						</Card>
						<WidgetPlaceholder class="w-1/3" />
					</div>
				</TabItem>
				<TabItem class="" disabled>
					{#snippet titleSlot()}
						<div
							class="mb-2.5 h-2.5 w-32 rounded-full bg-gray-200 dark:bg-gray-700 animate-pulse"
						></div>
					{/snippet}
				</TabItem>
			</Tabs>
			<!-- <div class="flex flex-wrap gap-10">
			<CardPlaceholder size="lg" class="w-1/3" />
			<WidgetPlaceholder class="w-1/3" />
		</div> -->
		{:then _}
			<div class="flex flex-wrap justify-between">
				<!-- max-w-sm is 24 rem, so make max heading width slightly smaller -->
				<Heading class="flex break-words max-w-[calc(100%-25rem)]" tag="h1"
					>{data.title}
					<A
						class="text-black dark:text-white hover:text-primary-500 dark:hover:text-primary-500"
						href="https://github.com/{data.title}"><GithubSolid class="ml-2 h-full w-10" /></A
					></Heading
				>
				<!-- <Select underline items={snapshots} bind:value={selected} class="max-w-sm min-w-sm" /> -->
			</div>
			<Hr />
			<Tabs classes={{ content: 'bg-white dark:bg-gray-800 p-0' }}>
				<TabItem open title="Overview">
					{#if !('version' in (projectData?.[selected] ?? {}))}
						{#if Object.keys(bak?.[selected] ?? {}).length <= 0 && !bak[selected]}
							<P size="lg">There is currently no overview data available for this snapshot.</P>
						{:else}
							<Overview data={bak} {avg} bind:selected {project_id} {snapshots} />
						{/if}
					{:else}
						<Overview data={projectData} {avg} bind:selected {snapshots} />
					{/if}
				</TabItem>
				<TabItem title="Details">
					<Details data={{ data: projectData, bak: bak, md: data.md }} bind:selected {snapshots} />
				</TabItem>
			</Tabs>
		{/await}
	</div>
	<!-- h-[calc(65vh))] -->
	<div class="w-1/5 ml-auto h-[calc(65vh))] sticky top-10">
		<Heading tag="h4" class="mx-5 mb-5">Snapshots</Heading>
		<Table hoverable divClass="shadow-none overflow-y-visible h-full scrollbar" striped={true}>
			<!-- <Table shadow={false} border={false}> -->
			<!-- <TableHead class="">
			<TableHeadCell class="flex"><P>Snapshots</P></TableHeadCell>
		</TableHead> -->
			<TableBody class="">
				{#await Promise.all([data.projects, data.avg])}
					<TableBodyRow>
						<TableBodyCell><Skeleton></Skeleton></TableBodyCell>
					</TableBodyRow>
				{:then _}
					{#each snapshots.toReversed() as item}
						<TableBodyRow
							onclick={(e) => {
								selected = e.target.dataset.value;
								console.log(e.target);
							}}
						>
							<TableBodyCell
								class="whitespace-normal {item.value == selected
									? 'dark:bg-gray-900 bg-gray-100 text-primary-600'
									: ''}"
								data-value={item.value}>{item.name}</TableBodyCell
							>
						</TableBodyRow>
					{/each}
				{/await}
			</TableBody>
			<!-- </Table> -->
		</Table>
	</div>
</div>

<!-- modal for displaying the charts -->
<!-- <Modal
	title={chartOptions.series[0].name}
	bind:open={drawerHidden}
	size="lg"
	autoclose
	outsideclose={true}
	classes={{ header: !showChart ? 'hidden' : '', body: !showChart ? 'p-0 md:p-0 border-0' : '' }}
>
	<div class="chart-container {!showChart ? 'hidden' : ''}">
		<Chart options={chartOptions} size="lg" />
	</div>

	<Drawer
		placement="right"
		transitionParams={transitionParamsRight}
		bind:open={drawerHidden}
		outsideclose={showChart ? true : false}
		id="sidebar6"
		modal={false}
		dismissable={false}
		class="{!showChart ? 'backdrop:bg-black/50' : ''} fixed top-0 left-0 !z-50 h-auto p-0"
	>
		<div class="flex items-center border-b-1 border-gray-300 dark:border-gray-700 py-2" use:onShown>
			<CloseButton onclick={() => (showChart = false)} class="mr-auto " />
		</div>
		<div class="overflow-auto w-full h-full p-2 scrollbar">
			{@html overlayMD}
		</div>
	</Drawer>
</Modal> -->

<!-- a sidebar for showing the metric documentation -->
<!-- backdrop={!showChart ? true : false} -->

<style>
	:global(.apexcharts-svg) {
		overflow: visible;
	}
	.chart-container {
		padding-left: 5rem;
		margin-right: 5rem;
	}
	:global(.scrollbar) {
		overflow: auto;
		scrollbar-width: thin;
		scrollbar-color: light-dark(black, white) light-dark(lightslategray, darkslategray);
	}
</style>

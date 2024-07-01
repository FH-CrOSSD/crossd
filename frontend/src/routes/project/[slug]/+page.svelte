<script lang="ts">
	import { chartOptions } from '$lib/chartOptions';
	import { processMD, toFixed2 } from '$lib/util';
	import { Chart, CloseButton, Drawer, Heading, Hr, Modal, P, Select } from 'flowbite-svelte';
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

	/** @type {import('./$types').PageData */
	export let data: {
		title: string;
		data: [{ [key: string]: any }];
		bak: [{ [key: string]: any }];
		md: [{ [key: string]: any }];
	};

	let project_id: string;
	let snapshots: Array<{ value: number; name: string }>;
	let selected: string;
	let overlayID: string;
	let showChart: Boolean = false;
	let showDefinition: Boolean = false;
	let overlayMD: string;
	let scrollFinished = false;
	let drawerHidden = true;

	// hide drawer if there is no definition to show or if the chart should not be shown
	$: {
		drawerHidden = showDefinition === true ? !showChart : true;
	}
	// transition for the drawer (sidebar)
	const transitionParamsRight = {
		x: 320,
		duration: 200,
		easing: sineIn
	};

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
		drawerHidden = false;
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
	$: {
		snapshots = data.snapshots;
		updateSelected();
	}

	// whener data.bak changes
	// retrieve the project id, which is used in all bak metrics
	// elephant_factor is always there, so we chose it to retrieve the project id
	$: {
		if (data.bak) {
			project_id = Object.keys(data.bak[selected]?.elephant_factor ?? [])[0];
		}
	}

	// unsubscribe from the overlayStore when user leaves the page
	onDestroy(() => {
		console.log('the component is being destroyed');
		unsubscribe();
	});
</script>

<div class="">
	<div class="flex flex-wrap justify-between">
		<!-- max-w-sm is 24 rem, so make max heading width slightly smaller -->
		<Heading class="max-w-fit break-words max-w-[calc(100%-25rem)]" tag="h1">{data.title}</Heading>
		<Select underline items={snapshots} bind:value={selected} class="max-w-sm min-w-sm" />
	</div>
	<Hr />
	<div class="flex flex-wrap gap-4">
		<!-- show cards if there is data for them -->
		{#if Object.keys(data.data?.[selected] ?? {}).length > 0}
			<GenericMetricCard data={data.data} {selected} />
		{/if}
		{#if data.bak[selected]}
			<GenericBakCard data={data.bak} bind:selected {project_id} />
			<PullRequestCard data={data.bak} {selected} {project_id} />
			<ProjectVelocityCard data={data.bak} {selected} {project_id} />
			<CommunityHealthCard data={data.bak} {selected} {project_id} />
			{#if Object.keys(data.bak[selected]['issues']).length > 0}
				<IssueCard data={data.bak} {selected} {project_id} />
			{/if}
			{#if Object.keys(data.bak[selected]['contributions_distributions']).length > 0}
				<DistributionContributionCard data={data.bak} {selected} {project_id} />
			{/if}
			<LifecycleBranchesCard data={data.bak} {selected} {project_id} />
			<SecurityAdvisoriesCard data={data.bak} {selected} {project_id} />
		{/if}
		<!-- show when no data is available -->
		{#if Object.keys(data.data?.[selected] ?? {}).length <= 0 && !data.bak[selected]}
			<P size="lg">There is currently no data available for this snapshot.</P>
		{/if}
	</div>
</div>

<!-- modal for displaying the charts -->
<Modal
	title={chartOptions.series[0].name}
	bind:open={showChart}
	size="lg"
	autoclose
	outsideclose={true}
>
	<div class="chart-container">
		<Chart options={chartOptions} size="lg" />
	</div>
</Modal>

<!-- a sidebar for showing the metric documentation -->
<Drawer
	placement="right"
	transitionType="fly"
	transitionParams={transitionParamsRight}
	bind:hidden={drawerHidden}
	backdrop={!showChart ? true : false}
	activateClickOutside={!showChart ? true : false}
	id="sidebar6"
>
	<div class="flex items-center" use:onShown>
		<CloseButton on:click={() => (drawerHidden = true)} class="mb-4 dark:text-white" />
	</div>
	{@html overlayMD}
</Drawer>

<style>
	:global(.apexcharts-svg) {
		overflow: visible;
	}
	.chart-container {
		padding-left: 5rem;
		margin-right: 5rem;
	}
</style>

<script lang="ts">
	import { CloseButton, Drawer, Modal, P } from 'flowbite-svelte';
	import { processMD, toFixed2 } from '$lib/util';
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
	import { chartOptions } from '$lib/chartOptions';
	import { Chart } from '@flowbite-svelte-plugins/chart';
	import { sineIn } from 'svelte/easing';

    export let data;
	export let selected: string;
	let project_id: string;
    let overlayID: string;
	let showChart: boolean = false;
	let showDefinition: boolean = false;
	let overlayMD: string;
	let scrollFinished = false;
	let drawerHidden = false;
    export let snapshots;
$: {
		if (data.bak) {
			project_id = Object.keys(data.bak[selected]?.elephant_factor ?? [])[0];
		}
	}

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
const transitionParamsRight = {
		x: 320,
		duration: 200,
		easing: sineIn
	};
$: {
		drawerHidden = showDefinition === true ? showChart : false;
		// drawerHidden;
		// console.log(showDefinition);
		// console.log(drawerHidden);
	}
	
</script>
<div class="flex flex-wrap gap-4">
		<!-- show cards if there is data for them -->
		{#if Object.keys(data.data?.[selected] ?? {}).length > 0}
			<GenericMetricCard data={data.data} {selected} />
		{/if}
		{#if !('version' in (data.data?.[selected] ?? {}))}
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
		{:else if data.data[selected]['version'].split('.')[0] === '2'}
			<GenericBakCard data={data.data} bind:selected />
			<PullRequestCard data={data.data} {selected} />
			<ProjectVelocityCard data={data.data} {selected} />
			<CommunityHealthCard data={data.data} {selected} />
			{#if Object.keys(data.data[selected]['issues']).length > 0}
				<IssueCard data={data.data} {selected} />
			{/if}
			{#if Object.keys(data.data[selected]['contributions_distributions']).length > 0}
				<DistributionContributionCard data={data.data} {selected} />
			{/if}
			<LifecycleBranchesCard data={data.data} {selected} />
			<SecurityAdvisoriesCard data={data.data} {selected} />
		{/if}
	</div>

    <Modal
	title={chartOptions.series[0].name}
	bind:open={drawerHidden}
	size="lg"
	autoclose
	outsideclose={true}
	class="ml-[calc(50%-428px-(320px/2))]"
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
</Modal>

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

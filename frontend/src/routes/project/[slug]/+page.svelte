<script lang="ts">
	import { chartOptions } from '$lib/chartOptions';
	import { processMD, toFixed2 } from '$lib/util';
	import { Chart, CloseButton, Drawer, Heading, Hr, Modal, Select } from 'flowbite-svelte';
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

	let workflow_statuses: { [key: string]: any } = {};
	let project_id: string;
	let snapshots: Array<{ value: number; name: string }>;
	let selected: string;
	let overlayID: string;
	let showChart: Boolean = false;
	let showDefinition: Boolean = false;
	let overlayMD: string;
	let scrollFinished = false;
	let drawerHidden = true;
	// open and close modal along with drawer, if chart should be shown
	// let modalOpen = false;
	$:{drawerHidden=showDefinition===true?!showChart:true;}
	const transitionParamsRight = {
		x: 320,
		duration: 200,
		easing: sineIn
	};

	let unsubscribe = overlayStore.subscribe((value) => {
		console.log('store sub');
		if (value) {
			showChart = value.chart;
			showDefinition = value.definition;
			console.log(value);
			if (value.definition === true) {
				console.log("show def");
				overlayID = value.current_id;
				goToDefinition(value.current_md);
				// scroll(value.current_id);
			}
			if (value.chart === true) {
				prepareChart(value.current_id);
			}
			$overlayStore = null;
		}
	});

	function updateSelected() {
		selected = snapshots && snapshots.length > 0 ? snapshots[snapshots.length - 1]['value'] : 0;
	}

	async function goToDefinition(md: string) {
		overlayMD = (
			await processMD(
				data.md['metrics'][md + '.md']['text'] + '\n\n' + data.md['footnotes']['text']
			)
		).toString();
		drawerHidden = false;
	}

	function prepareChart(id: string) {
		const elem = document.querySelector('[data-id="' + id + '"]');
		chartOptions.series[0].name = elem ? elem.innerText : 'Data:';
		console.log(snapshots);
		chartOptions.series[0].data = snapshots.map((x) => {
			console.log(x);
			let val = $clickedSelector(x.value);
			return val % 1 === 0 ? val : toFixed2(val);
		}).filter(item => !(item === undefined || item === null));
		console.log(chartOptions.series[0].data);
		chartOptions.xaxis.categories = snapshots.filter(item => {
			let val = $clickedSelector(item.value);
			return !(val === undefined || val === null)
		}).map((x) => {
			return new Date(Date.parse(x.name)).toLocaleString('eo');
		});
		// modalOpen = true;
	}

	async function scroll() {
		console.log('scroll');
		document.getElementById(overlayID).scrollIntoView();
		scrollFinished = true;
	}

	/** @type {import('svelte/action').Action}  */
	function onShown(node) {
		// the node has been mounted in the DOM
		const observer = new IntersectionObserver((entries) => {
			if (entries[0].isIntersecting) {
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

	// $: modalOpen = showChart;
	$: {
		snapshots = data.snapshots;
		updateSelected();
	}
	// $: {
	// 	snapshots = [];
	// 	for (let i = 0; i < data.data.length; i++) {
	// 		snapshots.push({ value: i, name: new Date(data.data[i].timestamp * 1000).toUTCString() });
	// 	}
	// 	console.log('creating snapshots');
	// 	//change selected variable inside a function, because Svelte reactivity is triggered when changing var directly
	// 	//(always changed to last value)
	// 	updateSelected();
	// }

	$: {
		if (data.bak) {
			project_id = Object.keys(data.bak[selected]?.elephant_factor ?? [])[0];
		}
	}
	$: {
		workflow_statuses = {};
		if (data.data && Object.keys(data.data).length > 0) {
			// console.log(snapshots);
			// console.log(data.data[selected]);
			// console.log(selected);
			console.log(data.data);
			for (const [key, value] of Object.entries(
				data.data[selected]?.current_state_workflows ?? {}
			) as [[string, { [key: string]: any }]]) {
				if (!(value['conclusion'] in workflow_statuses)) {
					workflow_statuses[value['conclusion']] = 1;
				} else {
					workflow_statuses[value['conclusion']]++;
				}
			}
		}
	}

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
	</div>
</div>


<!-- outsideclose only if drawer not shown, otherwise you need to double close -->
	<!-- outsideclose={drawerHidden ? true : false} -->

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
<Drawer
	placement="right"
	transitionType="fly"
	transitionParams={transitionParamsRight}
	bind:hidden={drawerHidden}
	backdrop={!showChart?true:false}
	activateClickOutside={!showChart?true:false}
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

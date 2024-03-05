<script lang="ts">
	import { Modal, Chart } from 'flowbite-svelte';
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
	let selected: number;

	function updateSelected() {
		selected = snapshots ? snapshots[snapshots.length - 1]['value'] : 0;
	}

	$: {
		snapshots = [];
		for (let i = 0; i < data.data.length; i++) {
			snapshots.push({ value: i, name: new Date(data.data[i].timestamp * 1000).toUTCString() });
		}
		console.log('creating snapshots');
		//change selected variable inside a function, because Svelte reactivity is triggered when changing var directly
		//(always changed to last value)
		updateSelected();
		// selected = snapshots ? snapshots[snapshots.length - 1]['value']:0;
	}

	$: {
		if (data.bak && data.bak.length >= 1) {
			project_id = Object.keys(data.bak[selected]['elephant_factor'])[0];
		}
	}
	$: {
		workflow_statuses = {};
		if (data.data) {
			for (const [key, value] of Object.entries(data.data[selected]['current_state_workflows']) as [
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
	import { Alert, Button, Card, Hr } from 'flowbite-svelte';
	import { Heading, P, A, Mark, Secondary } from 'flowbite-svelte';
	import Bool from '$lib/Bool.svelte';
	import { Select, Label } from 'flowbite-svelte';

	import {
		CheckCircleSolid,
		CloseCircleSolid,
		ThumbsUpSolid,
		ThumbsDownSolid,
		QuestionCircleSolid
	} from 'flowbite-svelte-icons';
	function osiIcon(type: string) {
		switch (type) {
			case 'osi_approved':
				return ThumbsUpSolid;
			case 'not_osi_approved':
				return ThumbsDownSolid;
			case 'not_found':
				return QuestionCircleSolid;
		}
	}
	function toFixed2(value: any) {
		if (typeof value === 'number') {
			return value.toFixed(2);
		} else {
			return value;
		}
	}

	let bakGenericDataFn = (category: string, project_id: string, entry: string | null) => {
		return (selected: number) => {
			if (entry) {
				return data.bak[selected][category][project_id][entry];
			} else {
				return data.bak[selected][category][project_id];
			}
			// console.log(project_id);
		};
	};

	// let content = '';
	// let current_id = '';
	// let current_text = '';
	import MetricRow from './MetricRow.svelte';
	import { clickedSelector, overlayStore } from './Row.svelte';

	import type { overlayData } from '$lib/types';
	let overlayID: string;
	import { onDestroy } from 'svelte';
	onDestroy(() => {
		console.log('the component is being destroyed');
		unsubscribe();
	});
	let unsubscribe = overlayStore.subscribe((value) => {
		console.log('store sub');
		if (value) {
			console.log(value);
			if (value.definition) {
				overlayID = value.current_id;
				goToDefinition(value.current_md);
				// scroll(value.current_id);
			}
			if (value.chart) {
				prepareChart(value.current_id);
			}
			overlayStore.set(null);
		}
	});

	// let overlayData = {
	// 	content: '',
	// 	current_id: '',
	// 	current_md: '',
	// 	current_text: '',
	// 	mEvent: null,
	// 	chart: false,
	// 	definition: false
	// };
	// S: {
	// 	console.log("overlay");
	// 	if (overlayData.definition) {
	// 		goToDefinition(overlayData.mEvent);
	// 	}
	// 	if (overlayData.chart) {
	// 		prepareChart();
	// 	}
	// }
	let overlayMD: string;
	async function goToDefinition(md: string) {
		// let md = '';
		// if (
		// 	event.target.nodeName.toLowerCase() === 'path' ||
		// 	event.target.nodeName.toLowerCase() === 'strong'
		// ) {
		// 	// overlayData.current_id = event.target.parentElement.dataset['id'];
		// 	// md = event.target.parentElement.dataset['md'];
		// 	// overlayData.current_text = event.target.parentElement.innerText;
		// } else if (event.target.nodeName.toLowerCase() === 'svg') {
		// 	// overlayData.current_id = event.target.dataset['id'];
		// 	// md = event.target.dataset['md'];
		// 	overlayData.current_text = event.target.innerText;
		// }
		console.log('Definition');
		console.log(md);
		overlayMD = (
			await processMD(
				data.md['metrics'][md + '.md']['text'] + '\n\n' + data.md['footnotes']['text']
			)
		).toString();
		hidden6 = false;

		// options.series[0].name = overlayData.current_text;
		// options.series[0].data = snapshots.map((x) => {
		// 	let val = get(clickedSelector)(x.value);
		// 	return val % 1 === 0 ? val : toFixed2(val);
		// });
		// options.xaxis.categories = snapshots.map((x) => {
		// 	return new Date(Date.parse(x.name)).toLocaleString('eo');
		// });
		// event.preventDefault();
	}

	function prepareChart(id: string) {
		// options.series[0].name = overlayData.current_text;
		const elem = document.querySelector('[data-id="' + id + '"]');
		options.series[0].name = elem ? elem.innerText : 'Data:';
		console.log(snapshots);
		options.series[0].data = snapshots.map((x) => {
			console.log(x);
			let val = get(clickedSelector)(x.value);
			return val % 1 === 0 ? val : toFixed2(val);
		});
		options.xaxis.categories = snapshots.map((x) => {
			return new Date(Date.parse(x.name)).toLocaleString('eo');
		});
		modalOpen = true;
	}

	let scrollFinished = false;
	async function scroll() {
		console.log('scroll');
		document.getElementById(overlayID).scrollIntoView();
		scrollFinished = true;
	}
	import { InfoCircleOutline } from 'flowbite-svelte-icons';
	import { Drawer, CloseButton } from 'flowbite-svelte';
	import { InfoCircleSolid, ArrowRightOutline } from 'flowbite-svelte-icons';
	import { sineIn } from 'svelte/easing';
	import { processMD } from '$lib/util';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { get } from 'svelte/store';

	let hidden6 = true;
	$: modalOpen = !hidden6;
	let modalOpen = false;
	let transitionParamsRight = {
		x: 320,
		duration: 200,
		easing: sineIn
	};

	//   $:{
	// 	console.log(hidden6);
	// 	if(hidden6===false){
	// 		console.log(current_id);
	// 	scroll(null);}
	//   }

	/** @type {import('svelte/action').Action}  */
	function onShown(node) {
		// the node has been mounted in the DOM
		const observer = new IntersectionObserver((entries) => {
			if (entries[0].isIntersecting) {
				// element in viewport
				console.log('aasd');
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

	//   onMount(() =>{
	// let targetNode=document.getElementById("sidebar6");
	// var observer = new MutationObserver(function(){
	// if(targetNode.style.display != 'none'){
	//     // doSomething
	// 	scroll(null);
	// }
	// });
	// observer.observe(targetNode, { attributes: true, childList: true });
	//   });
	import MetricLabel from './MetricLabel.svelte';
	import GenericMetricCard from './GenericMetricCard.svelte';
	let options = {
		chart: {
			height: '400px',
			maxWidth: '100%',
			type: 'line',
			fontFamily: 'Inter, sans-serif',
			dropShadow: {
				enabled: false
			},
			toolbar: {
				show: false
			}
		},
		tooltip: {
			enabled: true,
			x: {
				show: false
			},
			marker: {
				show: true
			}
			// 		custom: function({ series, seriesIndex, dataPointIndex, w }) {
			//   return (
			//     '<div class="arrow_box">' +
			//     "<span>" +
			//     w.globals.labels[dataPointIndex] +
			//     ": " +
			//     series[seriesIndex][dataPointIndex] +
			//     "</span>" +
			//     "</div>"
			//   );
			// }
		},
		dataLabels: {
			enabled: false
		},
		stroke: {
			width: 6,
			curve: 'smooth'
		},
		grid: {
			show: true,
			strokeDashArray: 4,
			padding: {
				left: 2,
				right: 2,
				top: -26
			}
		},
		series: [
			{
				// name: 'Clicks',
				data: [6500, 6418, 6456, 6526, 6356, 6456],
				color: '#1A56DB'
			}
		],
		legend: {
			show: false
		},
		xaxis: {
			categories: ['01 Feb', '02 Feb', '03 Feb', '04 Feb', '05 Feb', '06 Feb', '07 Feb'],
			labels: {
				show: true,
				style: {
					fontFamily: 'Inter, sans-serif',
					cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400'
				}
			},
			axisBorder: {
				show: false
			},
			axisTicks: {
				show: false
			}
		},
		yaxis: {
			show: true
		}
	};
</script>

<!-- <MetricLabel
						click={goToDefinition}
						data_id="a--total-number-of-branches-per-state-adopted"
						data_md="branches">Pull Requests (median):</MetricLabel
					> -->
<div class="">
	<div class="flex flex-wrap justify-between">
		<Heading class="max-w-fit break-words" tag="h1">{data.title}</Heading>
		<Select underline items={snapshots} bind:value={selected} class="max-w-sm min-w-sm" />
	</div>
	<Hr />
	<!-- <div class="grid grid-flow-col auto-cols-fr auto-rows-auto gap-4"> -->
	<div class="flex flex-wrap gap-4">
		{#if data.data}
			<GenericMetricCard click={goToDefinition} data={data.data} bind:selected />
			<!-- <Card class="max-w-xl">
				<div class="grid gap-y-4 gap-x-12 max-w-xl grid-cols-[max-content_max-content]">
					<MetricLabel click={goToDefinition}>Pull Requests (mean):</MetricLabel>
					<P class="max-w-xs">{data.data[selected]['mean_pull_requests']}</P>
					<MetricLabel click={goToDefinition}>Pull Requests (median):</MetricLabel>
					<P class="max-w-xs">{data.data[selected]['median_pull_requests']}</P>
					<MetricLabel click={goToDefinition}>Dependents:</MetricLabel>
					<P class="max-w-xs">{data.data[selected]['dependents_count']}</P>
					<MetricLabel click={goToDefinition}>Dependencies:</MetricLabel>
					<P class="max-w-xs">{data.data[selected]['dependencyCount']}</P>
					<MetricLabel click={goToDefinition}>Feature Requests:</MetricLabel>
					<P class="max-w-xs">{data.data[selected]['feature_request_count']}</P>
					<MetricLabel click={goToDefinition}>Closed Feature Requests:</MetricLabel>
					<P class="max-w-xs">{data.data[selected]['closed_feature_request_count']}</P>
					<MetricLabel click={goToDefinition}>Security Policy:</MetricLabel>
					<P class="max-w-xs"><Bool value={data.data[selected]['has_security_policy']} /></P>
					<MetricLabel click={goToDefinition}>Contribution Policy:</MetricLabel>
					<P class="max-w-xs"><Bool value={data.data[selected]['has_contributing_policy']} /></P>
					<MetricLabel click={goToDefinition}>Collaboration Platform:</MetricLabel>
					<P class="max-w-xs"><Bool value={data.data[selected]['has_collaboration_platform']} /></P>
					<MetricLabel click={goToDefinition}>Fundable:</MetricLabel>
					<P class="max-w-xs"><Bool value={data.data[selected]['is_fundable']} /></P>
					<MetricLabel click={goToDefinition}>Workflows:</MetricLabel>
					<P class="max-w-xs"><Bool value={data.data[selected]['uses_workflows']} /></P>
					{#if data.data[selected]['uses_workflows']}
						<MetricLabel click={goToDefinition}>Workflow Statuses:</MetricLabel>
						<P class="max-w-xs">
							{#each Object.entries(workflow_statuses) as status}
								{status[1]} {status[0]}<br />
							{/each}
						</P>
					{/if}
				</div>
			</Card> -->
		{/if}
		{#if data.bak}
			<Card class="max-w-xl">
				<div class="grid gap-y-4 gap-x-12 max-w-xl grid-cols-[max-content_max-content]">
					<MetricRow
						data_id="elephant-factor"
						data_md="elephant_factor"
						bind:selected
						selector={bakGenericDataFn('elephant_factor', project_id, null)}
						>Elephant factor:</MetricRow
					>
					<MetricLabel click={goToDefinition} data_id="elephant-factor" data_md="elephant_factor"
						>Elephant factor:</MetricLabel
					>
					<P class="max-w-xs">{data.bak[selected]['elephant_factor'][project_id]}</P>
					<MetricLabel click={goToDefinition} data_id="churn" data_md="churn">Churn:</MetricLabel>
					<P class="max-w-xs">{toFixed2(data.bak[selected]['churn'][project_id])}</P>
					<MetricLabel
						click={goToDefinition}
						data_id="size-of-community"
						data_md="size_of_community">Community size:</MetricLabel
					>
					<P class="max-w-xs">{data.bak[selected]['size_of_community'][project_id]}</P>
					<MetricLabel
						click={goToDefinition}
						data_id="number-of-support-contributors"
						data_md="number_of_support_contributors">Support contributors:</MetricLabel
					>
					<P class="max-w-xs">{data.bak[selected]['number_of_support_contributors'][project_id]}</P>
					<MetricLabel click={goToDefinition} data_id="maturity-level" data_md="maturity_level"
						>Maturity level:</MetricLabel
					>
					<P class="max-w-xs">{toFixed2(data.bak[selected]['maturity_level'][project_id])}</P>
					<MetricLabel
						data_id="osi-approved-licenses"
						data_md="osi_approved_licenses"
						click={goToDefinition}>OSI approved license:</MetricLabel
					>
					<P class="max-w-xs">
						<svelte:component
							this={osiIcon(data.bak[selected]['osi_approved_license'][project_id])}
						/>
					</P>
					<MetricLabel
						click={goToDefinition}
						data_id="criticality-score"
						data_md="criticality_score">Criticality score:</MetricLabel
					>
					<P class="max-w-xs">{data.bak[selected]['criticality_score'][project_id]}</P>
					<MetricRow
						click={goToDefinition}
						data_id="support-rate"
						data_md="support_rate"
						bind:selected
						selector={bakGenericDataFn('support_rate', project_id, null)}>Support rate:</MetricRow
					>
					<MetricLabel click={goToDefinition} data_id="support-rate" data_md="support_rate"
						>Support rate:</MetricLabel
					>
					<P class="max-w-xs">{toFixed2(data.bak[selected]['support_rate'][project_id])}</P>
					<MetricLabel
						click={goToDefinition}
						data_id="a--upstream-dependencies-adapted"
						data_md="code_dependencies">Code dependency upstream:</MetricLabel
					>
					<P class="max-w-xs"
						>{data.bak[selected]['code_dependency'][project_id]['total_upstream']}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_id="b--downstream-dependencies-created"
						data_md="code_dependencies">Code dependency downstream:</MetricLabel
					>
					<P class="max-w-xs"
						>{data.bak[selected]['code_dependency'][project_id]['total_downstream']}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_id="a--total-number-of-created-forks-adopted"
						data_md="technical_fork">Total forks:</MetricLabel
					>
					<P class="max-w-xs">{data.bak[selected]['technical_fork'][project_id]['total_forks']}</P>
					<MetricLabel
						click={goToDefinition}
						data_id="b--average-forks-created-per-week-created"
						data_md="technical_fork">Average forks per week:</MetricLabel
					>
					<P class="max-w-xs"
						>{data.bak[selected]['technical_fork'][project_id]['average_forks_created_per_week']}</P
					>
				</div>
			</Card>
			<Card size="lg">
				<Heading tag="h5" class="mb-4">Pull requests (PR)</Heading>
				<div class="grid gap-y-4 gap-x-12 max-w-xl grid-cols-[max-content_max-content]">
					<MetricLabel
						click={goToDefinition}
						data_id="a--total-pulls-adopted"
						data_md="change_pull_request">Total PR:</MetricLabel
					>
					<P class="max-w-xs">{data.bak[selected]['pull_requests'][project_id]['total_pulls']}</P>
					<MetricRow
						click={goToDefinition}
						data_id="b--average-pull-closing-time-created"
						data_md="change_pull_request"
						bind:selected
						selector={bakGenericDataFn('pull_requests', project_id, 'avg_pull_closing_days')}
						>Average days for closing PR:</MetricRow
					>
					<MetricLabel
						click={goToDefinition}
						data_id="b--average-pull-closing-time-created"
						data_md="change_pull_request">Average days for closing PR:</MetricLabel
					>
					<P class="max-w-xs"
						>{toFixed2(data.bak[selected]['pull_requests'][project_id]['avg_pull_closing_days'])}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_id="c--open-to-total-pull-requests-ratio-created"
						data_md="change_pull_request">Ratio open PR:</MetricLabel
					>
					<P class="max-w-xs"
						>{toFixed2(data.bak[selected]['pull_requests'][project_id]['ratio_open_total'])}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_id="d--closed-to-total-pull-requests-ratio-created"
						data_md="change_pull_request">Ratio closed PR:</MetricLabel
					>
					<P class="max-w-xs"
						>{toFixed2(data.bak[selected]['pull_requests'][project_id]['ratio_closed_total'])}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_id="e--merged-to-total-pull-requests-ratio-created"
						data_md="change_pull_request">Ratio merged PR:</MetricLabel
					>
					<P class="max-w-xs"
						>{toFixed2(data.bak[selected]['pull_requests'][project_id]['ratio_merged_total'])}</P
					>
				</div>
			</Card>
			<Card size="lg">
				<Heading tag="h5" class="mb-4">Project velocity</Heading>
				<div class="grid grid-cols-[max-content_max-content] gap-y-4 gap-x-12 max-w-xl">
					<MetricLabel
						click={goToDefinition}
						data_md="project_velocity"
						data_id="a--number-of-total-issues-adopted">Total issues:</MetricLabel
					>
					<P class="max-w-xs"
						>{data.bak[selected]['project_velocity'][project_id]['total_issues']}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="project_velocity"
						data_id="b--number-of-closed-issues-adopted">Closed issues:</MetricLabel
					>
					<P class="max-w-xs"
						>{data.bak[selected]['project_velocity'][project_id]['closed_issues']}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="project_velocity"
						data_id="c--number-of-open-issues-created">Open issues:</MetricLabel
					>
					<P class="max-w-xs">{data.bak[selected]['project_velocity'][project_id]['open_issues']}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="project_velocity"
						data_id="d--number-of-total-pull-requests-in-issues-created">Pull count:</MetricLabel
					>
					<P class="max-w-xs">{data.bak[selected]['project_velocity'][project_id]['pull_count']}</P>
					<MetricLabel
						click={goToDefinition}
						data_md="project_velocity"
						data_id="e-number-of-total-issues-which-are-no-pull-request-created"
						>No pull count:</MetricLabel
					>
					<P class="max-w-xs"
						>{data.bak[selected]['project_velocity'][project_id]['no_pull_count']}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="project_velocity"
						data_id="f--number-pull-request-to-total-issues-ratio-created"
						>Ratio pull issue:</MetricLabel
					>
					<P class="max-w-xs"
						>{toFixed2(data.bak[selected]['project_velocity'][project_id]['ratio_pull_issue'])}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="project_velocity"
						data_id="g--average-issue-closing-time-created"
						>Average days for resolving issue:</MetricLabel
					>
					<P class="max-w-xs"
						>{data.bak[selected]['project_velocity'][project_id]['avg_issue_resolving_days']}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="project_velocity"
						data_id="h--open-issues-to-total-issues-ratio-created">Ratio open issues:</MetricLabel
					>
					<P class="max-w-xs"
						>{toFixed2(data.bak[selected]['project_velocity'][project_id]['ratio_open_total'])}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="project_velocity"
						data_id="i--closed-issues-to-total-issues-ratio-created"
						>Ratio closed issues:</MetricLabel
					>
					<P class="max-w-xs"
						>{toFixed2(data.bak[selected]['project_velocity'][project_id]['ratio_closed_total'])}</P
					>
				</div>
			</Card>
			<Card size="lg">
				<Heading tag="h5" class="mb-4">Github community health</Heading>
				<div class="grid grid-cols-[max-content_max-content] gap-y-4 gap-x-12 max-w-xl">
					<MetricLabel
						click={goToDefinition}
						data_md="github_community_health_percentage"
						data_id="a--github-community-health-percentage-score-adopted"
						>Community Health score:</MetricLabel
					>
					<P
						>{data.bak[selected]['github_community_health_percentage'][project_id][
							'community_health_score'
						]}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="github_community_health_percentage"
						data_id="b--custom-github-community-health-percentage-score-adapted"
						>Custom Health score:</MetricLabel
					>
					<P class="max-w-xs"
						>{data.bak[selected]['github_community_health_percentage'][project_id][
							'custom_health_score'
						]}</P
					>
					<!-- <MetricLabel click={goToDefinition}>True count:</MetricLabel>
				<P class="max-w-xs">{data.bak[data.bak.length-1]['github_community_health_percentage'][project_id]['true_count']}</P>
				<MetricLabel click={goToDefinition}>False count:</MetricLabel>
				<P class="max-w-xs">{data.bak[data.bak.length-1]['github_community_health_percentage'][project_id]['false_count']}</P> -->
					<MetricLabel
						click={goToDefinition}
						data_md="github_community_health_percentage"
						data_id="c--existence-of-single-documents-and-information-created"
						>Has description:</MetricLabel
					>
					<P
						><Bool
							value={data.bak[selected]['github_community_health_percentage'][project_id][
								'description'
							]}
						/>
					</P>
					<MetricLabel
						click={goToDefinition}
						data_md="github_community_health_percentage"
						data_id="c--existence-of-single-documents-and-information-created"
						>Has documentation:</MetricLabel
					>
					<P
						><Bool
							value={data.bak[selected]['github_community_health_percentage'][project_id][
								'documentation'
							]}
						/></P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="github_community_health_percentage"
						data_id="c--existence-of-single-documents-and-information-created"
						>Has code of conduct:</MetricLabel
					>
					<P
						><Bool
							value={data.bak[selected]['github_community_health_percentage'][project_id][
								'code_of_conduct'
							]}
						/></P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="github_community_health_percentage"
						data_id="c--existence-of-single-documents-and-information-created"
						>Has contributing:</MetricLabel
					>
					<P
						><Bool
							value={data.bak[selected]['github_community_health_percentage'][project_id][
								'contributing'
							]}
						/></P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="github_community_health_percentage"
						data_id="c--existence-of-single-documents-and-information-created"
						>Has issue templates:</MetricLabel
					>
					<P
						><Bool
							value={data.bak[selected]['github_community_health_percentage'][project_id][
								'issue_template'
							]}
						/></P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="github_community_health_percentage"
						data_id="c--existence-of-single-documents-and-information-created"
						>Has PR templates:</MetricLabel
					>
					<P
						><Bool
							value={data.bak[selected]['github_community_health_percentage'][project_id][
								'pull_request_template'
							]}
						/></P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="github_community_health_percentage"
						data_id="c--existence-of-single-documents-and-information-created"
						>Has license:</MetricLabel
					>
					<P
						><Bool
							value={data.bak[selected]['github_community_health_percentage'][project_id][
								'license'
							]}
						/></P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="github_community_health_percentage"
						data_id="c--existence-of-single-documents-and-information-created"
						>Has README:</MetricLabel
					>
					<P
						><Bool
							value={data.bak[selected]['github_community_health_percentage'][project_id]['readme']}
						/></P
					>
				</div>
			</Card>
			<Card size="lg">
				<Heading tag="h5" class="mb-4">Issues</Heading>
				<div class="grid grid-cols-[max-content_max-content] gap-y-4 gap-x-12 max-w-xl">
					<MetricLabel
						click={goToDefinition}
						data_md="issues"
						data_id="e--number-of-total-issues-created">Total issues:</MetricLabel
					>
					<P class="max-w-xs">{data.bak[selected]['issues'][project_id]['total_issues']}</P>
					<MetricLabel
						click={goToDefinition}
						data_md="issues"
						data_id="f--number-of-open-issues-created">Open issues:</MetricLabel
					>
					<P class="max-w-xs">{data.bak[selected]['issues'][project_id]['open_issues']}</P>
					<MetricLabel
						click={goToDefinition}
						data_md="issues"
						data_id="c--number-of-closed-issues-adopted">Closed issues:</MetricLabel
					>
					<P class="max-w-xs">{data.bak[selected]['issues'][project_id]['closed_issues']}</P>
					<MetricLabel
						click={goToDefinition}
						data_md="issues"
						data_id="a--number-of-newcreated-issues-adopted">New issues:</MetricLabel
					>
					<P class="max-w-xs">{data.bak[selected]['issues'][project_id]['new_issues']}</P>
					<MetricLabel
						click={goToDefinition}
						data_md="issues"
						data_id="b--new-issues-to-total-issues-ratio-adopted">Ratio new issues:</MetricLabel
					>
					<P class="max-w-xs">{toFixed2(data.bak[selected]['issues'][project_id]['new_ratio'])}</P>
					<MetricLabel
						click={goToDefinition}
						data_md="issues"
						data_id="h--average-issues-created-per-week-created"
						>Average issues created per week:</MetricLabel
					>
					<P class="max-w-xs"
						>{data.bak[selected]['issues'][project_id]['average_issues_created_per_week']}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="issues"
						data_id="i--average-issue-comments-created">Average comments per issue:</MetricLabel
					>
					<P class="max-w-xs"
						>{data.bak[selected]['issues'][project_id]['average_issue_comments']}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="issues"
						data_id="j--average-issue-resolving-days-created"
						>Average days for resolving issues:</MetricLabel
					>
					<P class="max-w-xs"
						>{data.bak[selected]['issues'][project_id]['average_issue_resolving_days']}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="issues"
						data_id="k--average-first-response-time-in-days-created"
						>Average days for first response:</MetricLabel
					>
					<P class="max-w-xs"
						>{data.bak[selected]['issues'][project_id]['average_first_response_time_days']}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="issues"
						data_id="g--open-issues-to-total-issues-ratio-created">Ratio open issues:</MetricLabel
					>
					<P class="max-w-xs"
						>{toFixed2(data.bak[selected]['issues'][project_id]['ratio_open_total'])}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="issues"
						data_id="d--closed-issues-to-total-issues-ratio-adopted"
						>Ratio closed issues:</MetricLabel
					>
					<P class="max-w-xs"
						>{toFixed2(data.bak[selected]['issues'][project_id]['ratio_closed_total'])}</P
					>
				</div>
			</Card>
			{#if Object.keys(data.bak[selected]['contributions_distributions']).length > 0}
				<Card size="lg">
					<Heading tag="h5" class="mb-4">Distribution of contributions</Heading>
					<div class="grid grid-cols-[max-content_max-content] gap-y-4 gap-x-12 max-w-xl">
						<MetricLabel
							click={goToDefinition}
							data_md="contributions_distributions"
							data_id="b--pareto-principle-rof--noc-adopted">Ratio of files tail:</MetricLabel
						>
						<P class="max-w-xs"
							>{toFixed2(
								data.bak[selected]['contributions_distributions'][project_id]['RoF_tail']
							)}</P
						>
						<MetricLabel
							click={goToDefinition}
							data_md="contributions_distributions"
							data_id="b--pareto-principle-rof--noc-adopted">Ratio of files dominant:</MetricLabel
						>
						<P class="max-w-xs"
							>{toFixed2(
								data.bak[selected]['contributions_distributions'][project_id]['RoF_dominant']
							)}</P
						>
						<MetricLabel
							click={goToDefinition}
							data_md="contributions_distributions"
							data_id="b--pareto-principle-rof--noc-adopted"
							>Ratio of files diff percentage:</MetricLabel
						>
						<P
							>{toFixed2(
								data.bak[selected]['contributions_distributions'][project_id]['RoF_diff_percent']
							)}</P
						>
						<MetricLabel
							click={goToDefinition}
							data_md="contributions_distributions"
							data_id="c--average-contributors-per-file-adapted"
							>Average contributors per file:</MetricLabel
						>
						<P
							>{toFixed2(
								data.bak[selected]['contributions_distributions'][project_id][
									'avg_num_contributors_per_file'
								]
							)}</P
						>
						<MetricLabel
							click={goToDefinition}
							data_md="contributions_distributions"
							data_id="a--bus-factor-adopted">Bus factor score:</MetricLabel
						>
						<P class="max-w-xs"
							>{data.bak[selected]['contributions_distributions'][project_id][
								'bus_factor_score'
							]}</P
						>
						<MetricLabel
							click={goToDefinition}
							data_md="contributions_distributions"
							data_id="b--pareto-principle-rof--noc-adopted">Number of commits tail:</MetricLabel
						>
						<P class="max-w-xs"
							>{toFixed2(
								data.bak[selected]['contributions_distributions'][project_id]['NoC_tail']
							)}</P
						>
						<MetricLabel
							click={goToDefinition}
							data_md="contributions_distributions"
							data_id="b--pareto-principle-rof--noc-adopted"
							>Number of commits dominant:</MetricLabel
						>
						<P class="max-w-xs"
							>{toFixed2(
								data.bak[selected]['contributions_distributions'][project_id]['NoC_dominant']
							)}</P
						>
						<MetricLabel
							click={goToDefinition}
							data_md="contributions_distributions"
							data_id="b--pareto-principle-rof--noc-adopted"
							>Number of commits diff percentage:</MetricLabel
						>
						<P
							>{toFixed2(
								data.bak[selected]['contributions_distributions'][project_id]['NoC_diff_percent']
							)}</P
						>
					</div>
				</Card>
			{/if}

			<Card size="lg">
				<Heading tag="h5" class="mb-4">Lifecycle of branches</Heading>
				<div class="grid grid-cols-[max-content_max-content] gap-y-4 gap-x-12 max-w-xl">
					<MetricLabel
						click={goToDefinition}
						data_md="branches"
						data_id="e--branch-creation-frequency-created"
						>Frequency of branch creation (days):</MetricLabel
					>
					<P class="max-w-xs"
						>{data.bak[selected]['branch_lifecycle'][project_id][
							'branch_creation_frequency_days'
						]}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="branches"
						data_id="b--average-branch-age-adopted">Average age of branches (days) :</MetricLabel
					>
					<P class="max-w-xs"
						>{data.bak[selected]['branch_lifecycle'][project_id]['branch_avg_age_days']}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="branches"
						data_id="f--stale-branch-to-total-branch-ratio-created"
						>Ratio stale branches:</MetricLabel
					>
					<P class="max-w-xs"
						>{toFixed2(data.bak[selected]['branch_lifecycle'][project_id]['stale_ratio'])}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="branches"
						data_id="g--active-branch-to-total-branch-ratio-created"
						>Ratio active branches:</MetricLabel
					>
					<P class="max-w-xs"
						>{toFixed2(data.bak[selected]['branch_lifecycle'][project_id]['active_ratio'])}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="branches"
						data_id="d--unresolved-branch-to-total-branch-ratio-adapted"
						>Ratio unresolved branches:</MetricLabel
					>
					<P class="max-w-xs"
						>{toFixed2(data.bak[selected]['branch_lifecycle'][project_id]['unresolved_ratio'])}</P
					>
					<MetricLabel
						click={goToDefinition}
						data_md="branches"
						data_id="c--resolved-branch-to-total-branch-ratio-adapted"
						>Ratio resolved branches:</MetricLabel
					>
					<P class="max-w-xs"
						>{toFixed2(data.bak[selected]['branch_lifecycle'][project_id]['resolved_ratio'])}</P
					>
					<!-- <MetricLabel click={goToDefinition}>Branch state counter:</MetricLabel>
					<P class="max-w-xs"
						>{data.bak[selected]['branch_lifecycle'][project_id][
							'branch_state_counter'
						]}</P
					> -->
				</div>
			</Card>
			<Card size="lg">
				<Heading tag="h5" class="mb-4">Security advisories</Heading>
				<div class="grid grid-cols-[max-content_max-content] gap-y-4 gap-x-12 max-w-xl">
					{#if Object.keys(data.bak[selected]['security_advisories'][0][project_id]).length === 0}
						<MetricLabel
							click={goToDefinition}
							data_md="security_advisories"
							data_id="b--existing-advisories-created">Advisories available:</MetricLabel
						>
						<P class="max-w-xs">No</P>
					{:else}
						<MetricLabel
							click={goToDefinition}
							data_md="security_advisories"
							data_id="b--existing-advisories-created">Advisories available:</MetricLabel
						>
						<P
							>{data.bak[selected]['security_advisories'][0][project_id]['advisories_available']
								? 'Yes'
								: 'No'}</P
						>
						<MetricLabel
							click={goToDefinition}
							data_md="security_advisories"
							data_id="c--patched-advisories-to-total-advisories-ratio-created"
							>Ratio patched:</MetricLabel
						>
						<P class="max-w-xs"
							>{data.bak[selected]['security_advisories'][0][project_id]['patch_ratio']}</P
						>
						<MetricLabel
							click={goToDefinition}
							data_md="security_advisories"
							data_id="d--number-of-closed-advisories-created">Number of closed:</MetricLabel
						>
						<P class="max-w-xs"
							>{data.bak[selected]['security_advisories'][0][project_id]['closed_advisories']}</P
						>
						<MetricLabel
							click={goToDefinition}
							data_md="security_advisories"
							data_id="a--average-cvss-score-adopted">Average CVSS score:</MetricLabel
						>
						<P class="max-w-xs"
							>{toFixed2(
								data.bak[selected]['security_advisories'][0][project_id]['average_cvss_score']
							)}</P
						>
						<MetricLabel
							click={goToDefinition}
							data_md="security_advisories"
							data_id="e--advisories-with-critical-or-high-severity-to-total-advisories-ratio-created"
							>Ratio high or critical severity:</MetricLabel
						>
						<P
							>{toFixed2(
								data.bak[selected]['security_advisories'][0][project_id]['ratio_severity_high_crit']
							)}</P
						>
					{/if}
				</div>
			</Card>
		{/if}
	</div>
</div>

<Drawer
	placement="right"
	transitionType="fly"
	transitionParams={transitionParamsRight}
	bind:hidden={hidden6}
	id="sidebar6"
>
	<div class="flex items-center" use:onShown>
		<CloseButton on:click={() => (hidden6 = true)} class="mb-4 dark:text-white" />
	</div>
	{@html overlayMD}
</Drawer>

<Modal title={options.series[0].name} bind:open={modalOpen} size="lg" autoclose>
	<div class="chart-container">
		<Chart {options} size="lg" />
	</div>
</Modal>

<style>
	:global(.apexcharts-svg) {
		overflow: visible;
	}
	.chart-container {
		padding-left: 5rem;
		margin-right: 5rem;
	}
</style>

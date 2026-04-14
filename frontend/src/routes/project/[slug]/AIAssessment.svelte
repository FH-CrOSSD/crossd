<script lang="ts">
	import MetricCard from './MetricCard.svelte';
	import MetricRow from './MetricRow.svelte';
	import { bakGenericDataFn as bgdFn, toFixed2 } from '$lib/util';
	import { Alert, Heading, Hr, Indicator, List, Listgroup, P, Tooltip, Li } from 'flowbite-svelte';
	import FloatMetricRow from './FloatMetricRow.svelte';
	import MetricValue from './MetricValue.svelte';
	import { chartOptions } from '$lib/chartOptions';
	import { clickedSelector, overlayStore } from './Row.svelte';
	import { Chart } from '@flowbite-svelte-plugins/chart';
	import { ExclamationCircleOutline, InfoCircleSolid } from 'flowbite-svelte-icons';

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
	let val = (key: string, value: string) => {
		return (selected: number) => {
			return ai[selected]['result']?.[key]?.[value] ?? null;
		};
	};
</script>

<Alert color="amber" class="mb-4 py-2">
	{#snippet icon()}<ExclamationCircleOutline class="h-5 w-5" />{/snippet}
	These metrics are generated using artificial intelligence operating on repository data and may contain
	errors or inaccuracies.
	<br />We do not guarantee its completeness or reliability.
</Alert>
<div class="flex flex-wrap gap-10">
	<!-- {JSON.stringify(ai,null,4)} -->
	<MetricCard cardClass="min-w-[48%]">
		<svelte:fragment slot="heading">
			<div class="place-content-between grid grid-cols-2">
				{ai[selected]['result']['friendliness']['display_name']}
				<InfoCircleSolid class="shrink-0 h-6 w-6 ml-auto text-gray-400" />
				<Tooltip
					class="max-w-md bg-gray-200 border-gray-300 dark:bg-gray-600 dark:border-gray-500"
					trigger="click"
				>
					<P class="text-base font-bold mb-2">LLM instructions (w/o data)</P>
					<P class="leading-normal">
						Evaluate how friendly and welcoming the repository developers are when interacting with
						contributors and users in issues and comments. Consider tone, responsiveness,
						helpfulness, and encouragement. Give a score from 1 to 10 where 1 is hostile/unwelcoming
						and 10 is exceptionally friendly and supportive.
					</P>
				</Tooltip>
			</div>
		</svelte:fragment>
		<MetricRow bind:selected selector={val('friendliness', 'metric')}>Metric:</MetricRow>
		<br />
		<!-- <MetricRow bind:selected selector={val("friendliness","explanation")}>Explanation:</MetricRow> -->
		<svelte:fragment slot="remainder"
			><P>Explanation:</P><P><br />{ai[selected]['result']['friendliness']['explanation']}</P>
		</svelte:fragment>
	</MetricCard>
	<MetricCard cardClass="min-w-[48%]">
		<svelte:fragment slot="heading">
			<div class="place-content-between grid grid-cols-2">
				{ai[selected]['result']['documentation_quality']['display_name']}
				<InfoCircleSolid class="shrink-0 h-6 w-6 ml-auto text-gray-400" />
				<Tooltip
					class="max-w-md bg-gray-200 border-gray-300 dark:bg-gray-600 dark:border-gray-500"
					trigger="click"
				>
					<P class="text-base font-bold mb-2">LLM instructions (w/o data)</P>
					<P class="leading-normal">
						Analyse the quality of documentation in this repository. Consider the README structure,
						whether there are contributing guides, code of conduct, issue/PR templates, and external
						docs links. Give a score from 1 to 10 where 1 is poor and 10 is excellent.
					</P>
				</Tooltip>
			</div>
		</svelte:fragment>
		<MetricRow bind:selected selector={val('documentation_quality', 'metric')}>Metric:</MetricRow>
		<br />
		<!-- <MetricRow bind:selected selector={val("documentation_quality","explanation")}>Explanation:</MetricRow> -->
		<svelte:fragment slot="remainder"
			><P>Explanation:</P><P
				><br />{ai[selected]['result']['documentation_quality']['explanation']}</P
			></svelte:fragment
		>
	</MetricCard>
	<MetricCard cardClass="min-w-[48%]">
		<svelte:fragment slot="heading">
			<div class="place-content-between grid grid-cols-2">
				{ai[selected]['result']['development_efficiency']['display_name']}
				<InfoCircleSolid class="shrink-0 h-6 w-6 ml-auto text-gray-400" />
				<Tooltip
					class="max-w-md bg-gray-200 border-gray-300 dark:bg-gray-600 dark:border-gray-500"
					trigger="click"
				>
					<P class="text-base font-bold mb-2">LLM instructions (w/o data)</P>
					<P class="leading-normal">
						Evaluate how efficiently development is conducted in this repository. Consider issue
						resolution time, PR turnaround, branching strategy, release cadence, commit activity,
						and contributor productivity. Give a score from 1 to 10 where 1 is very inefficient and
						10 is highly efficient.
					</P>
				</Tooltip>
			</div></svelte:fragment
		>
		<MetricRow bind:selected selector={val('development_efficiency', 'metric')}>Metric:</MetricRow>
		<br />
		<!-- <MetricRow bind:selected selector={val("development_efficiency","explanation")}>Explanation:</MetricRow> -->
		<svelte:fragment slot="remainder"
			><P>Explanation:</P><P
				><br />{ai[selected]['result']['development_efficiency']['explanation']}</P
			></svelte:fragment
		>
	</MetricCard>
	<MetricCard cardClass="min-w-[48%]">
		<svelte:fragment slot="heading">
			<div class="place-content-between grid grid-cols-2">
				{ai[selected]['result']['project_maturity']['display_name']}
				<InfoCircleSolid class="shrink-0 h-6 w-6 ml-auto text-gray-400" />
				<Tooltip
					class="max-w-md bg-gray-200 border-gray-300 dark:bg-gray-600 dark:border-gray-500"
					trigger="click"
				>
					<P class="text-base font-bold mb-2">LLM instructions (w/o data)</P>
					<P class="leading-normal">
						Evaluate the overall maturity of this open-source project. Score holistically across ALL
						of the following dimensions — no single dimension should dominate:
						<List class="my-2">
							<Li>Governance: code of conduct, contributing guide, issue/PR templates</Li>
							<Li>Community: contributor count, bus-factor, PR activity, issue responsiveness</Li>
							<Li>Release & versioning: release history, cadence, tagging</Li>
							<Li>Documentation: README quality, external docs, changelogs</Li>
							<Li>CI/CD & automation: automated tests, build pipelines</Li>
							<Li
								>Security posture: security policy presence, advisory count/severity, patch
								responsiveness — treat this as ONE of the six dimensions above, not a veto over the
								others.</Li
							>
						</List>
						Give a score from 1 to 100 in increments of 0.1 where 1 is very immature and 100 is a fully
						mature project.
					</P>
				</Tooltip>
			</div>
		</svelte:fragment>
		<MetricRow bind:selected selector={val('project_maturity', 'metric')}>Metric:</MetricRow>
		<FloatMetricRow {selected} selector={bakGenericDataFn('maturity_level', project_id)}
			>Maturity level: <br /> <span class="text-amber-600">(non-AI metric)</span></FloatMetricRow
		>
		<br />
		<!-- <MetricRow bind:selected selector={val("project_maturity","explanation")}>Explanation:</MetricRow> -->
		<svelte:fragment slot="remainder"
			><P>Explanation:</P><P><br />{ai[selected]['result']['project_maturity']['explanation']}</P
			></svelte:fragment
		>
	</MetricCard>
</div>

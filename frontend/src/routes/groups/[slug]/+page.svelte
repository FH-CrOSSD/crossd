<script lang="ts">
	import { A, Badge, Card, CardPlaceholder, Heading, Hr, P, Skeleton } from 'flowbite-svelte';
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

	let { data }: PageProps = $props();
	let test = $state();
	data.group.then((val) => (test = val));

	let searchTerm = $state('');
	let filteredItems = $derived.by(() => {
		return test?.projects?.filter(
			(item) => !searchTerm || item.toLowerCase().includes(searchTerm.toLowerCase())
		);
	});
	let activeClass="inline-block text-sm font-medium text-center disabled:cursor-not-allowed active p-4 text-primary-600 bg-gray-100 rounded-t-lg dark:bg-gray-900 dark:text-primary-500";

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
			<Tabs style="underline" class="w-full" contentClass="bg-white dark:bg-gray-800">
				<TabItem open title="Avg" {activeClass}>
					<Statistics
						{...{
							name: data.name,
							count: test?.projects?.length,
							elephant_factor: group.data.avg.elephant_factor,
							maturity_level: group.data.avg.maturity_level,
							criticality_score: group.data.avg.criticality_score,
							support_rate: group.data.avg.support_rate,
							github_community_health_percentage: group.data.avg.github_community_health_percentage
						}}
					/>
				</TabItem>
				<TabItem title="Min" {activeClass}>
					<Statistics
						{...{
							name: data.name,
							count: test?.projects?.length,
							elephant_factor: group.data.min.elephant_factor,
							maturity_level: group.data.min.maturity_level,
							criticality_score: group.data.min.criticality_score,
							support_rate: group.data.min.support_rate,
							github_community_health_percentage: group.data.min.github_community_health_percentage
						}}
					/>
				</TabItem>
				<TabItem title="Max" {activeClass}>
					<Statistics
						{...{
							name: data.name,
							count: test?.projects?.length,
							elephant_factor: group.data.max.elephant_factor,
							maturity_level: group.data.max.maturity_level,
							criticality_score: group.data.max.criticality_score,
							support_rate: group.data.max.support_rate,
							github_community_health_percentage: group.data.max.github_community_health_percentage
						}}
					/>
				</TabItem>
				<TabItem title="Agg" {activeClass}>
					<Statistics
						{...{
							name: data.name,
							count: test?.projects?.length,
							elephant_factor: group.data.sum.elephant_factor,
							maturity_level: group.data.sum.maturity_level,
							criticality_score: group.data.sum.criticality_score,
							support_rate: group.data.sum.support_rate,
							github_community_health_percentage: group.data.sum.github_community_health_percentage
						}}
					/>
				</TabItem>
				<TabItem title="Stddev" {activeClass}>
					<Statistics
						{...{
							name: data.name,
							count: test?.projects?.length,
							elephant_factor: group.data.stddev.elephant_factor,
							maturity_level: group.data.stddev.maturity_level,
							criticality_score: group.data.stddev.criticality_score,
							support_rate: group.data.stddev.support_rate,
							github_community_health_percentage: group.data.stddev.github_community_health_percentage
						}}
					/>
				</TabItem>
			</Tabs>
		{/await}
	</div>
	<!-- <div>
		<Heading tag="h1" class="mb-4"
			>Group <span class="bg-gray-200 dark:bg-gray-600 px-1 rounded-md">{data.name}</span></Heading
		>
		<div class="flex flex-wrap gap-10">
			<Card class="p-5 h-fit w-fit">
				<Heading tag="h4" class="mb-5">Stats</Heading>
				{#await data.group}
					<Skeleton size="sm" class="my-5"></Skeleton>
				{:then group}
					<div class="grid gap-y-4 gap-x-12 max-w-xl grid-cols-[max-content_max-content]">
						{console.log(group.data)}
						<P class="max-w-60">Repository count:</P>
						<P class="max-w-60">{test?.projects?.length}</P>
						<P class="max-w-60">Elephant factor:</P>
						<P class="max-w-60">{group.data.elephant_factor}</P>
						<P class="max-w-60">Maturity level:</P>
						<P class="max-w-60">{group.data.maturity_level}</P>
						<P class="max-w-60">Criticality score:</P>
						<P class="max-w-60">{group.data.criticality_score}</P>
						<P class="max-w-60">Support rate:</P>
						<P class="max-w-60">{group.data.support_rate}</P>
						<P class="max-w-60">Github community health:</P>
						<P class="max-w-60">{group.data.github_community_health_percentage}</P>
					</div>
				{/await}
			</Card>
			<Card class="p-5 h-fit w-fit">
				<Heading tag="h4" class="mb-5">Stats</Heading>
				{#await data.group}
					<Skeleton size="sm" class="my-5"></Skeleton>
				{:then group}
					<div class="grid gap-y-4 gap-x-12 max-w-xl grid-cols-[max-content_max-content]">
						{console.log(group.data)}
						<P class="max-w-60">Elephant factor:</P>
						<P class="max-w-60">{group.data.elephant_factor}</P>
						<P class="max-w-60">Maturity level:</P>
						<P class="max-w-60">{group.data.maturity_level}</P>
						<P class="max-w-60">Criticality score:</P>
						<P class="max-w-60">{group.data.criticality_score}</P>
						<P class="max-w-60">Support rate:</P>
						<P class="max-w-60">{group.data.support_rate}</P>
						<P class="max-w-60">Github community health:</P>
						<P class="max-w-60">{group.data.github_community_health_percentage}</P>
					</div>
				{/await}
			</Card>
			<Card class="p-5 h-fit w-fit">
				<Heading tag="h4" class="mb-5">Stats</Heading>
				{#await data.group}
					<Skeleton size="sm" class="my-5"></Skeleton>
				{:then group}
					<div class="grid gap-y-4 gap-x-12 max-w-xl grid-cols-[max-content_max-content]">
						{console.log(group.data)}
						<P class="max-w-60">Elephant factor:</P>
						<P class="max-w-60">{group.data.elephant_factor}</P>
						<P class="max-w-60">Maturity level:</P>
						<P class="max-w-60">{group.data.maturity_level}</P>
						<P class="max-w-60">Criticality score:</P>
						<P class="max-w-60">{group.data.criticality_score}</P>
						<P class="max-w-60">Support rate:</P>
						<P class="max-w-60">{group.data.support_rate}</P>
						<P class="max-w-60">Github community health:</P>
						<P class="max-w-60">{group.data.github_community_health_percentage}</P>
					</div>
				{/await}
			</Card>
			<Card class="p-5 h-fit w-fit">
				<Heading tag="h4" class="mb-5">Stats</Heading>
				{#await data.group}
					<Skeleton size="sm" class="my-5"></Skeleton>
				{:then group}
					<div class="grid gap-y-4 gap-x-12 max-w-xl grid-cols-[max-content_max-content]">
						{console.log(group.data)}
						<P class="max-w-60">Elephant factor:</P>
						<P class="max-w-60">{group.data.elephant_factor}</P>
						<P class="max-w-60">Maturity level:</P>
						<P class="max-w-60">{group.data.maturity_level}</P>
						<P class="max-w-60">Criticality score:</P>
						<P class="max-w-60">{group.data.criticality_score}</P>
						<P class="max-w-60">Support rate:</P>
						<P class="max-w-60">{group.data.support_rate}</P>
						<P class="max-w-60">Github community health:</P>
						<P class="max-w-60">{group.data.github_community_health_percentage}</P>
					</div>
				{/await}
			</Card>
			<Card class="p-5 h-fit w-fit">
				<Heading tag="h4" class="mb-5">Stats</Heading>
				{#await data.group}
					<Skeleton size="sm" class="my-5"></Skeleton>
				{:then group}
					<div class="grid gap-y-4 gap-x-12 max-w-xl grid-cols-[max-content_max-content]">
						{console.log(group.data)}
						<P class="max-w-60">Elephant factor:</P>
						<P class="max-w-60">{group.data.elephant_factor}</P>
						<P class="max-w-60">Maturity level:</P>
						<P class="max-w-60">{group.data.maturity_level}</P>
						<P class="max-w-60">Criticality score:</P>
						<P class="max-w-60">{group.data.criticality_score}</P>
						<P class="max-w-60">Support rate:</P>
						<P class="max-w-60">{group.data.support_rate}</P>
						<P class="max-w-60">Github community health:</P>
						<P class="max-w-60">{group.data.github_community_health_percentage}</P>
					</div>
				{/await}
			</Card>
		</div>
	</div> -->
	<div class="max-w-1/4 w-1/4 ml-auto">
		<Heading tag="h4" class="mx-5 mt-5">Group repositories</Heading>
		<TableSearch
			placeholder="Search by name"
			hoverable
			bind:inputValue={searchTerm}
			divClass="shadow-none"
			tableClass=""
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

<script lang="ts">
	import {
		Card,
		CardPlaceholder,
		Heading,
		Hr,
		P,
		Skeleton,
		TextPlaceholder
	} from 'flowbite-svelte';

	/** @type {import('./$types').PageData */
	/** @type {import('./$types').PageData */
	export let data: {
		data: [{ [key: string]: any }];
	};
</script>

{console.log(data)}

<div class="flex gap-5">
	{#await data.stream}
		<Card class="p-3 h-38">
			<Skeleton size="sm" class=""></Skeleton>
		</Card>
		<Card class="p-3 h-38">
			<Skeleton size="sm" class=""></Skeleton>
		</Card>
	{:then groups}
		{#each groups.data as group}
			<Card size="xs" class="h-38 p-2" href="/groups/{group.group.name}">
				<Heading tag="h5" class="">{group.group.name}</Heading>
				<Hr class="w-full my-1" />
				<P># of projects: {group.projects.length}</P>
			</Card>
		{/each}
	{/await}
</div>

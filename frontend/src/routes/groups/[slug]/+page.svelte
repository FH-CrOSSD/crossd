<script lang="ts">
	import { Card, Heading, Hr, P } from 'flowbite-svelte';
	import {
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
		TableSearch
	} from 'flowbite-svelte';

	/** @type {import('./$types').PageData */
	/** @type {import('./$types').PageData */
	export let data: {
		name: string;
		group: [{ [key: string]: any }];
	};

	let searchTerm = '';
	// let items = [
	// 	{ id: 1, maker: 'Toyota', type: 'ABC', make: 2017 },
	// 	{ id: 2, maker: 'Ford', type: 'CDE', make: 2018 },
	// 	{ id: 3, maker: 'Volvo', type: 'FGH', make: 2019 },
	// 	{ id: 4, maker: 'Saab', type: 'IJK', make: 2020 }
	// ];
	//   let filteredItems = $derived.by(() => items.filter((item) => !searchTerm || item.maker.toLowerCase().includes(searchTerm.toLowerCase())));
	$: filteredItems = data.group["projects"].filter(
		(item) => !searchTerm || item.toLowerCase().includes(searchTerm.toLowerCase())
	);
</script>

{console.log(data)}

<TableSearch placeholder="Search by name" hoverable bind:inputValue={searchTerm} divClass="w-1/3 ml-auto relative" tableClass="">
	<TableHead>
		<TableHeadCell>Repository</TableHeadCell>
	</TableHead>
	<TableBody>
		{#each filteredItems as item}
			<TableBodyRow>
				<TableBodyCell>{item}</TableBodyCell>
			</TableBodyRow>
		{/each}
	</TableBody>
</TableSearch>

<!-- <div class="flex">
    {#each data.data as group}
    <Card size="xs" class="h-20 px-2">
        <Heading tag="h5" class="">{group.group.name}</Heading>
        <Hr class="w-full my-1" />
        <P># of projects: {group.projects.length}</P>
    </Card>
    {/each}
</div> -->

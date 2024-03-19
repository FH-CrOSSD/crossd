<script lang="ts">
	import type { PageData } from './$types';
	import { Heading, P, A, Mark, Secondary } from 'flowbite-svelte';
	import { Listgroup, ListgroupItem } from 'flowbite-svelte';
	export let data: PageData;
	import SvelteMarkdown from 'svelte-markdown';
	import { Alert, Button, Search, Card, Hr } from 'flowbite-svelte';
	import { SearchOutline } from 'flowbite-svelte-icons';
	// console.log(data.results);
	// $: {
	// 	if (!Array.isArray(data['results'])) {
	// 		data['results'] = [];
	// 	}
	// }

	function get_readme(item: { [key: string]: any }): string {
		let res: string = '';
		const prepare = (x: { [key: string]: any }, index: string) =>
			x.repository.readmes[index]['text']
				.split(' ')
				.slice(0, 50)
				.join(' ')
				.replace(/<[^>]*>?/gm, '') + ' ...';

		if (!item.repository.readmes) {
			return res;
		}

		if ('README_md' in item.repository.readmes) {
			res = prepare(item, 'README_md');
		} else {
			for (let rm in item.repository.readmes) {
				if (item.repository.readmes[rm]) {
					res = prepare(item, rm);
				}
				break;
			}
		}
		return res;
	}
</script>

<div class="justify-center mb-10" style="object-position:bottom">
	<!-- transition:fly|global={{ y: '-200%', duration: 2000, opacity: 100 }} -->
	<Card padding="xl" class="mx-auto max-w-screen mt-10">
		<form method="GET" class="flex gap-0" action="/search">
			<Search class="rounded-r-none py-2.5" id="project" name="project" value={data['term']} />
			<Button class="pb-2 rounded-s-none" type="submit">
				<!-- type="submit" -->
				<SearchOutline class="w-5 h-5" />
				<Heading tag="h6" class="text-white ml-2">Search</Heading>
			</Button>
		</form>
	</Card>
</div>
<Hr />
<Heading tag="h1" class="mb-10">Search results:</Heading>
<Card size="xl" class="break-words max-w-full">
	<Listgroup>
		{#each data.results as item}
			<ListgroupItem>
				<div class="grid grid-cols-3 dark:divide-gray-700 divide-x">
					<div class="pr-5 col-span-1">
						<Heading tag="h4"
							><a href="/project/{encodeURIComponent(item.name)}">{item.name}</a></Heading
						>
						{#if item.timestamp}
							<P class="mt-4"
								><strong>Last Crawled:</strong> {new Date(item.timestamp * 1000).toUTCString()}</P
							>
						{/if}
					</div>

					<P class="px-5 col-span-2">
						{#if item.repository}
							{item.repository.description ? item.repository.description : get_readme(item)}
						{/if}
					</P>
				</div>
			</ListgroupItem>
		{:else}
			<ListgroupItem>No results found</ListgroupItem>
		{/each}
	</Listgroup>
</Card>

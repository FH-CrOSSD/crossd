<script lang="ts">
	import type { PageData } from './$types';
	import { Heading, P, A, Mark, Secondary } from 'flowbite-svelte';
	import { Card, Listgroup, ListgroupItem, Hr } from 'flowbite-svelte';
	export let data: PageData;
	import SvelteMarkdown from 'svelte-markdown';
	console.log(data.results);

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

<Heading tag="h1" class="mb-10">Search results:</Heading>
<Card size="xl" class="break-all">
	<Listgroup>
		{#each data.results as item}
			<ListgroupItem>
				<div class="grid grid-cols-2 divide-x">
					<div>
						<Heading tag="h4">{item.repository.nameWithOwner}</Heading>
						{#if item.timestamp}
							<P class="mt-4"
								><strong>Last Crawled:</strong> {new Date(item.timestamp * 1000).toUTCString()}</P
							>
						{/if}
					</div>
					<P class="px-5"
						>{item.repository.description ? item.repository.description : get_readme(item)}</P
					>
				</div>
			</ListgroupItem>
		{/each}

		<ListgroupItem>test</ListgroupItem>
	</Listgroup>
</Card>

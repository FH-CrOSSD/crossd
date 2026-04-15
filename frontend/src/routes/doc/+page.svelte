<script lang="ts">
	import { Sidebar, SidebarGroup, SidebarItem, SidebarWrapper } from 'flowbite-svelte';
	import { processMD } from '$lib/util';
	import type { PageData } from './$types';
	import { page } from '$app/stores';
	import { tick } from 'svelte';

	export let data: PageData;
	const metrics = Object.keys(data['metrics']).sort();
	// store markdown of all metrics and the footnotes inside a single string
	let fullText = '';
	for (let i = 0; i < metrics.length; i++) {
		fullText += data['metrics'][metrics[i]]['text'];
		fullText += '\n\n';
	}
	fullText += data['footnotes']['text'];

	$: activeUrl = $page.url.pathname;
</script>

<!-- processMD converts the markdown to html -->
{#await processMD(fullText) then doc}
	<div class="relative max-w-full flex">
		<div class="w-3/4">
			<!-- replaceAll fixes a remark/rehype plugin bug -->
			{@html doc.toString().replaceAll('user-content-user-content', 'user-content')}
		</div>
		<!-- wait until rendering is finished -->
		{#await tick() then}
			<!-- top-[118px] -->
			<div
				class="w-1/4 sticky ml-5 right-0 top-24 flex justify-end overflow-y-auto 2xl:h-[calc(75vh)] sm:h-[calc(55vh)] lg:h-[calc(65vh)] self-start md:flex"
			>
				<Sidebar {activeUrl} position="static" class="w-full scrollbar">
					<SidebarWrapper>
						<SidebarGroup>
							{#each document.getElementsByClassName('metric_heading') as heading}
								<SidebarItem label={heading.innerText} href="#{heading.id}" />
							{/each}
						</SidebarGroup>
					</SidebarWrapper>
				</Sidebar>
			</div>
		{/await}
	</div>
{/await}

<style>
	:global(.scrollbar) {
		overflow: auto;
		scrollbar-width: thin;
		scrollbar-color: light-dark(black, white) light-dark(lightslategray, darkslategray);
	}
</style>
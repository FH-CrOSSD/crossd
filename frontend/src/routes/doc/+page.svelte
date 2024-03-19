<script lang="ts">
    import { onMount } from 'svelte';
	// import rehypeStringify from 'rehype-stringify';
	// // import remarkFrontmatter from 'remark-frontmatter';
	// import remarkGfm from 'remark-gfm';
	// import remarkParse from 'remark-parse';
	// import remarkRehype from 'remark-rehype';
	// import remarkGridTables from 'remark-grid-tables';
	// import remarkMath from 'remark-math';
	// import rehypeKatex from 'rehype-katex';
	// import rehypeMathjax from 'rehype-mathjax';
	// import remarkGridTable from '@adobe/remark-gridtables';

	// const remarkGridTables = require('remark-grid-tables')
	// import { unified } from 'unified';
	// import { text } from './md/github_community_health_percentage';

	//     import remarkDirective from 'remark-directive';
	// import remarkDirectiveRehype from 'remark-directive-rehype';
	// import { A, P, Heading, Blockquote } from 'flowbite-svelte';
	import { Sidebar, SidebarGroup, SidebarItem, SidebarWrapper } from 'flowbite-svelte';
	// import { micromark } from 'micromark';
	// import { gfm, gfmHtml } from 'micromark-extension-gfm';
	// import { gfmTable, gfmTableHtml } from 'micromark-extension-gfm-table';
	// import { math, mathHtml } from 'micromark-extension-math';
	// import {gridTables, gridTablesHtml} from '@adobe/micromark-extension-gridtables';
	// import {directive, directiveHtml} from 'micromark-extension-directive';
	// const result = micromark(text.replaceAll('$$', ' $'), {
	// 	extensions: [gfm(), gfmTable(),math(),gridTables,directive()],
	// 	htmlExtensions: [gfmHtml(), gfmTableHtml(),mathHtml(),gridTablesHtml,directiveHtml()]
	// });
	// import rehypeSanitize from 'rehype-sanitize';
	// import remarkBreaks from 'remark-breaks';
	// import rehypeAutolinkHeadings from 'rehype-autolink-headings';
	// import rehypeSlug from 'rehype-slug';
	// import addClasses from 'rehype-add-classes';
	// import rehypeShiftHeading from 'rehype-shift-heading';
	import {processMD} from '$lib/util';
	const headingClasses = ' font-extrabold text-gray-900 dark:text-white w-full mt-5';
	// async function process(text: string) {
	// 	const file = await unified()
	// 		.use(remarkParse)
	// 		//     .use(remarkDirective)
	// 		// .use(remarkDirectiveRehype)

	// 		.use(remarkMath)
	// 		// .use(remarkGridTables)
	// 		.use(remarkGfm)
	// 		.use(remarkGridTable)
	// 		.use(remarkRehype)
	// 		.use(rehypeSanitize)
	// 		.use(rehypeKatex)
	// 		// .use(rehypeMathjax)
	// 		.use(rehypeSlug)
	// 		.use(rehypeAutolinkHeadings)
	// 		.use(rehypeShiftHeading, { shift: 1 })
	// 		.use(addClasses, {
	// 			p: 'text-base text-gray-900 dark:text-white leading-normal font-normal text-left whitespace-normal afterp',
	// 			h1: 'text-5xl' + headingClasses,
	// 			h2: 'text-4xl metric_heading' + headingClasses,
	// 			h3: 'text-3xl' + headingClasses,
	// 			h4: 'text-2xl' + headingClasses,
	// 			h5: 'text-xl' + headingClasses,
	// 			h6: 'text-lg' + headingClasses,
	// 			blockquote: "font-semibold text-gray-900 dark:text-white text-left text-lg bg-gray-50 dark:bg-gray-800 border-s-4 border-gray-300 dark:border-gray-500 italic p-4 my-4"
	// 		})
	// 		.use(rehypeStringify)
	// 		.process(text.replaceAll('$$', ' $'));
	// 	return file;
	// }
	import type { PageData } from './$types';
	export let data: PageData;
	// let res = process();
	// console.log(data);
	// console.log(Object.keys(data).sort());
	const metrics = Object.keys(data['metrics']).sort();
	let fullText = '';
	for (let i = 0; i < metrics.length; i++) {
		fullText += data['metrics'][metrics[i]]['text'];
		fullText += '\n\n';
	}
	fullText += data['footnotes']['text'];
	import { page } from '$app/stores';
	$: activeUrl = $page.url.pathname;

    onMount(async () => {
        console.log(document.getElementsByClassName("metricheading"));
        await new Promise(r => setTimeout(r, 100));
        const headings = document.getElementsByClassName("metricheading");
        
        for(let i=0;i<headings.length;i++){
            console.log(headings[i]);
            console.log("a");
        }
       
	});
    import { tick } from 'svelte';
</script>
<!-- <Sidebar {activeUrl}>
	<SidebarWrapper>
		<SidebarGroup>
			<SidebarItem label="Dashboard">
			</SidebarItem>
		</SidebarGroup>
	</SidebarWrapper>
</Sidebar> -->
{#await processMD(fullText) then doc}
<div class="relative max-w-full">
    <div class="w-3/4">
	{@html doc.toString().replaceAll('user-content-user-content', 'user-content')}
    </div>
    {#await tick() then}
    <!-- top-[118px] -->
	<div class="w-1/4 fixed right-0 top-[12.5%] flex justify-end overflow-y-scroll h-3/4 hidden md:flex">
    <Sidebar {activeUrl} class="w-full">
        <SidebarWrapper>
                <SidebarGroup>
                    {#each document.getElementsByClassName("metric_heading") as heading}
                         <SidebarItem label="{heading.innerText}" href="#{heading.id}">
                            asdasd
                    </SidebarItem>
                    {/each}
                </SidebarGroup>
            </SidebarWrapper>
    </Sidebar>
	</div>
    {/await}
    </div>
{/await}

<!-- {#each metrics as metric} -->
<!-- {#await process(data[metric]['text']) then doc} -->
<!-- {@html doc} -->
<!-- {/await} -->
<!-- <br /> -->
<!-- <br /> -->
<!-- {/each} -->
<!-- <style>
    :global(p.afterp) {margin-bottom: 1em;}
</style> -->

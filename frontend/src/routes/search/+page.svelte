<script lang="ts">
	import type { PageData } from './$types';
	import { Heading, P } from 'flowbite-svelte';
	import { Listgroup, ListgroupItem } from 'flowbite-svelte';
	export let data: PageData;
	import { Button, Search, Card, Hr } from 'flowbite-svelte';
	import { SearchOutline } from 'flowbite-svelte-icons';
	import { PER_PAGE } from '$lib/util';
	import { page } from '$app/stores';
	import { Pagination } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	function get_readme(item: { [key: string]: any }): string {
		let res: string = '';
		const prepare = (x: { [key: string]: any }, index: string) => {
			return x.repository.readmes[index]
				? x.repository.readmes[index]?.['text']
						.split(' ')
						.slice(0, 50)
						.join(' ')
						.replace(/<[^>]*>?/gm, '') + ' ...'
				: undefined;
		};

		if (!item.repository.readmes) {
			return res;
		}

		if ('README_md' in item.repository.readmes && item.repository.readmes['README_md']) {
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

	$: lastPage = Math.ceil(data.length / PER_PAGE);
	$: activePage = Number($page.url.searchParams.get('page')) || 1;
	$: {
		if (activePage < 1 || activePage > lastPage) {
			activePage = 1;
		}
	}

	$: base_url = $page.url.pathname + '?project=' + $page.url.searchParams.get('project');
	let pages;
	// prepare pages for pagination
	$: {
		pages = [];
		// first page - always
		pages.push({ name: 1, href: base_url + '&page=1' });

		// ... placeholder on the left side
		if (activePage > 4 && lastPage > 7) {
			pages.push({ name: '...', href: undefined });
		}

		// show 5 pages in between
		if (activePage <= 4) {
			// get first pages
			// insert 5 pages unless total pages is less
			for (let i = 2; i <= 6 && i <= lastPage - 1; i++) {
				pages.push({ name: i, href: base_url + '&page=' + i });
			}
		} else if (activePage > lastPage - 3) {
			// get last pages
			// insert 5 pages unless total pages is less
			for (let i = lastPage - 5 < 1 ? 2 : lastPage - 5; i <= lastPage - 1; i++) {
				pages.push({ name: i, href: base_url + '&page=' + i });
			}
		} else {
			// in between (-2 current +2)
			// insert 5 pages
			for (let i = activePage - 2; i <= activePage + 2 && i <= lastPage - 1; i++) {
				pages.push({ name: i, href: base_url + '&page=' + i });
			}
		}

		// ... placeholder on the right side
		if (activePage < lastPage - 3 && lastPage > 7) {
			pages.push({ name: '...', href: undefined });
		}

		// last page - always
		pages.push({
			name: lastPage,
			href: base_url + '&page=' + lastPage
		});
	}

	$: {
		pages.forEach((page) => {
			//set active (or not) status for each page
			if (page.href) {
				let splitUrl = page.href.split('?');
				let queryString = splitUrl.slice(1).join('?');
				const hrefParams = new URLSearchParams(queryString);
				let hrefValue = hrefParams.get('page');
				if (Number(hrefValue) === activePage) {
					page.active = true;
				} else {
					page.active = false;
				}
			} else {
				page.active = false;
			}
		});
		pages = pages;
	}

	const previous = () => {
		if (activePage > 1) {
			goto(base_url + '&page=' + (activePage - 1));
		}
		checkButtons(activePage - 1);
	};
	const next = () => {
		if (activePage < lastPage) {
			goto(base_url + '&page=' + (activePage + 1));
		}
		checkButtons(activePage + 1);
	};

	function removeHoverClasses(elem) {
		for (let i = 0; i < hoverClasses.length; i++) {
			elem.classList.remove(hoverClasses[i]);
		}
	}

	function addHoverClasses(elem) {
		for (let i = 0; i < hoverClasses.length; i++) {
			elem.classList.add(hoverClasses[i]);
		}
	}

	function checkButtons(page) {
		// handle disabling pagination buttons as flowbite-svelte does not provide this for their component
		if (page === 1) {
			document.querySelector('button:has(span#previous)').disabled = true;
			removeHoverClasses(document.querySelector('button:has(span#previous)'));
			document.querySelector('button:has(span#next)').disabled = false;
			addHoverClasses(document.querySelector('button:has(span#next)'));
		} else if (page === lastPage) {
			document.querySelector('button:has(span#next)').disabled = true;
			removeHoverClasses(document.querySelector('button:has(span#next)'));
			document.querySelector('button:has(span#previous)').disabled = false;
			addHoverClasses(document.querySelector('button:has(span#previous)'));
		} else {
			document.querySelector('button:has(span#next)').disabled = false;
			addHoverClasses(document.querySelector('button:has(span#next)'));
			document.querySelector('button:has(span#previous)').disabled = false;
			addHoverClasses(document.querySelector('button:has(span#previous)'));
		}
	}

	let hoverClasses = [];
	const click = (event) => {
		// when clicking on a pagination number
		checkButtons(Number(new URL(event.target.href).searchParams.get('page')));
	};

	onMount(async () => {
		// check pagination buttons on page load
		// copy classes, since we are modifying the array
		let classes = [...document.querySelector('button:has(span#previous)')?.classList];
		for (let i = 0; i < classes.length; i++) {
			if (classes[i].includes('hover:')) {
				hoverClasses.push(classes[i]);
			}
		}
		checkButtons(activePage);
	});
</script>

<div class="justify-center mb-10" style="object-position:bottom">
	<Card padding="xl" class="mx-auto max-w-screen mt-10">
		<form method="GET" class="flex gap-0" action="/search">
			<Search class="rounded-r-none py-2.5" id="project" name="project" value={data['term']} />
			<Button class="pb-2 rounded-s-none" type="submit">
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
{#if lastPage > 1}
	<div class="mt-10 mx-auto w-fit remove-nav-border">
		<Pagination {pages} large on:previous={previous} on:next={next} on:click={click}>
			<svelte:fragment slot="prev">
				<span id="previous">Previous</span>
			</svelte:fragment>
			<svelte:fragment slot="next">
				<span id="next">Next</span>
			</svelte:fragment>
		</Pagination>
	</div>
{/if}

<style>
	:global(.remove-nav-border > nav) {
		border-bottom-width: 0px;
	}
</style>

<script lang="ts">
	/** @type {import('./$types').PageData */
	export let data;
	import { toFixed2 } from '$lib/util';
	import { filesize } from 'filesize';
	import { Button, Card, Heading, Hr, P, Search } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	import { SearchOutline } from 'flowbite-svelte-icons';
	$: stats = data['results']['stats'];

	onMount(async () => {
		// autofocus input field
		document.getElementById("project")?.focus();
	});

</script>

<div class="justify-center" style="object-position:bottom">
	<Card class="mx-auto max-w-screen mt-10 p-4 sm:p-8">
		<form method="GET" class="flex gap-0" action="/search">
			<Search classes={{ input: "rounded-r-none py-2.5" }} id="project" name="project" />
			<Button class="pb-2 rounded-s-none" type="submit">
				<SearchOutline class="w-5 h-5" />
				<Heading tag="h6" class="text-white ml-2">Search</Heading>
			</Button>
		</form>
	</Card>
	<Hr />
	<div class="grid grid-col-1 justify-center items-center">
		<div>
			<Heading tag="h2" class="mb-4">Statistics</Heading>
			<div class="grid grid-cols-2 gap-x-6 gap-y-2">
				<P>Scanned projects:</P>
				<P class="max-w-fit">{stats['unique_projects']}</P>
				<P>Ø Scans per Project:</P>
				<P class="max-w-fit">{toFixed2(stats['avg_scans_per_project']) ?? 0}</P>
				<P>Size of Documents:</P>
				<P class="max-w-fit">{filesize(data['results']['figures']['docsSize'])}</P>
				<P>Number of Documents</P>
				<P class="max-w-fit">{data['results']['figures']['docsCount']}</P>
			</div>
		</div>
	</div>
</div>

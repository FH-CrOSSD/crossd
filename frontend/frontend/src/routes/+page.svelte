<script lang="ts">
	/** @type {import('./$types').PageData */
	export let data;
	import { Alert, Button, Search, Card, Hr } from 'flowbite-svelte';
	import { SearchOutline } from 'flowbite-svelte-icons';
	import { Heading, P, A, Mark, Secondary } from 'flowbite-svelte';
	import { toFixed2 } from '$lib/util';
	import {filesize} from "filesize";
	// import { fly, scale } from 'svelte/transition';
	let visible = true;
	console.log(data);
	$: stats = data['results']['stats'][0];
	// $:{stats = data['results'][0]};
</script>

<!-- <div class="p-8">
	<Alert color="red">
		<span class="font-medium">Info alert!</span>
		Change a few things up and try submitting again.
	</Alert>
</div> -->

<!-- <div class="p-8">
	<Button pill href="/project/Joplin">Joplin</Button>
</div> -->
<!-- h-screen -->
<div class="justify-center" style="object-position:bottom">
	<!-- transition:fly|global={{ y: '-200%', duration: 2000, opacity: 100 }} -->
	<Card padding="xl" class="mx-auto max-w-screen mt-10">
		<form method="GET" class="flex gap-0" action="/search">
			<Search class="rounded-r-none py-2.5" id="project" name="project" />
			<Button class="pb-2 rounded-s-none" type="submit">
				<!-- type="submit" -->
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
				<P class="max-w-fit">{toFixed2(stats['avg_scans_per_project'])}</P>
				<P>Size of Documents:</P>
				<P class="max-w-fit">{filesize(data['results']['figures']['docsSize'])}</P>
				<P>Number of Documents</P>
				<P class="max-w-fit">{data['results']['figures']['docsCount']}</P>
			</div>
		</div>
	</div>
</div>

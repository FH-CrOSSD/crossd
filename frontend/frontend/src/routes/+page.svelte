<script lang="ts">
	/** @type {import('./$types').PageData */
	export let data;
	import { Alert, Button, Search, Card } from 'flowbite-svelte';
	import { SearchOutline } from 'flowbite-svelte-icons';
	import { Heading, P, A, Mark, Secondary } from 'flowbite-svelte';
	// import { fly, scale } from 'svelte/transition';
	let visible = true;
</script>

<div class="p-8">
	<Alert color="red">
		<span class="font-medium">Info alert!</span>
		Change a few things up and try submitting again.
	</Alert>
</div>

<div class="p-8">
	<Button pill href="/project/Joplin">Joplin</Button>
</div>
<div class="justify-center" style="object-position:bottom">
	<!-- transition:fly={{ y: '-200%', duration: 2000, opacity: 100 }} -->
	<Card size="xl" padding="xl" class="mx-auto">
		<form method="GET" class="flex gap-0" action="/search">
			<Search class="rounded-r-none py-2.5" id="project" name="project"/>
			<Button class="pb-2 rounded-s-none" type="submit">
				<!-- type="submit" -->
				<SearchOutline class="w-5 h-5" />
				<Heading tag="h6" class="text-white ml-2">Search</Heading>
			</Button>
		</form>
	</Card>
</div>
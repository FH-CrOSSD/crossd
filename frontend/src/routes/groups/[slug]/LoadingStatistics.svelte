<script lang="ts">
	import { Card, Heading, Skeleton } from 'flowbite-svelte';
</script>

<div class="flex flex-wrap gap-10">
	<Card class="p-5 h-fit">
		<Heading tag="h4" class="mb-5">Stats</Heading>
		<Skeleton size="sm" class="my-5"></Skeleton>
	</Card>
</div>

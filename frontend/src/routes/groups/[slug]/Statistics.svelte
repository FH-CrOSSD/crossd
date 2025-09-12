<script lang="ts">
	import { Card, Heading, P } from 'flowbite-svelte';
	let {
		name,
		count,
		elephant_factor,
		maturity_level,
		criticality_score,
		support_rate,
		github_community_health_percentage
	} = $props();
</script>

<div class="flex flex-wrap gap-10">
	<Card class="p-5 h-fit w-fit">
		<Heading tag="h4" class="mb-5">Stats</Heading>
		<div class="grid gap-y-4 gap-x-12 max-w-xl grid-cols-[max-content_max-content]">
			<P class="max-w-60">Repository count:</P>
			<P class="max-w-60">{count}</P>
			<P class="max-w-60">Elephant factor:</P>
			<P class="max-w-60">{elephant_factor}</P>
			<P class="max-w-60">Maturity level:</P>
			<P class="max-w-60">{maturity_level}</P>
			<P class="max-w-60">Criticality score:</P>
			<P class="max-w-60">{criticality_score}</P>
			<P class="max-w-60">Support rate:</P>
			<P class="max-w-60">{support_rate}</P>
			<P class="max-w-60">Github community health:</P>
			<P class="max-w-60">{github_community_health_percentage}</P>
		</div>
	</Card>
</div>

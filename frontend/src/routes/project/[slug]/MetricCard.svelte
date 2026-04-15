<script lang="ts">
	import { Card, Heading } from 'flowbite-svelte';
	export let cardClass: string="max-w-[32%] max-lg:max-w-[45%] max-md:max-w-[70%]";
	export let gridColClass: string="grid-cols-[2fr_1fr]";
</script>

<Card class="p-4 sm:p-6 {cardClass}">
	<Heading tag="h5" class="mb-4"><slot name="heading" /></Heading>
	<!-- https://stackoverflow.com/questions/72432862/how-to-set-min-content-for-a-column-in-tailwind-css-grid -->
	<div class="grid gap-y-4 gap-x-8 max-w-xl {gridColClass}">
	<!-- grid-cols-[max-content_max-content] -->
		<slot />
	</div>
	<slot name="remainder"/>
</Card>

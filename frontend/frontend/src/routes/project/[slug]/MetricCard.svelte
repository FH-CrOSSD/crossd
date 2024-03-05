<script lang="ts">
	import { Card } from 'flowbite-svelte';
</script>

<Card class="max-w-xl">
	<!-- https://stackoverflow.com/questions/72432862/how-to-set-min-content-for-a-column-in-tailwind-css-grid -->
	<div class="grid gap-y-4 gap-x-12 max-w-xl grid-cols-[max-content_max-content]">
		<slot />
	</div>
</Card>

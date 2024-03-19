<script lang="ts">
	import { P } from 'flowbite-svelte';
	// import {MinusOutline} from 'flowbite-svelte-icons';

	export let value: any;
	$: mvalue = value?.toString() ?? '-';
</script>

<P class="max-w-60">
	{mvalue}
	<!-- {#if mvalue==='-'}
		<MinusOutline/>
	{:else}
		{mvalue}
	{/if} -->
</P>

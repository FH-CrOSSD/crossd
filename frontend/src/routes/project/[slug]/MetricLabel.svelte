<script lang="ts">
	import { A, P } from 'flowbite-svelte';
	export let click: any = null;
	export let data_md: string | null = null;
	export let data_id: string | null = null;
	export let chart: Boolean = false;
</script>

<P class="max-w-52">
	{#if click && (data_md || chart)}
		<A
			class="text-gray-900 dark:text-white underline hover:no-underline"
			onclick={click}
			data-md={data_md}
			data-id={data_id || ''}><strong><slot /></strong></A
		>
	{:else}
		<strong><slot /></strong>
	{/if}
</P>

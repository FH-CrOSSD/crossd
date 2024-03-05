<script lang="ts">
	import { P, A } from 'flowbite-svelte';
	import { InfoCircleOutline } from 'flowbite-svelte-icons';
	export let click: any;
	export let data_md: string | null = null;
	export let data_id: string | null = null;
	export let chart:Boolean=false;
	// export let overlayData;
	// function onClick(event){
	// 	overlayData = {...overlayData,...{mEvent:event,current_id:data_id,current_md:data_md,definition:true,chart:true}}
	// }
</script>

<P class="max-w-xs">
	{#if data_md || chart}
		<A
			class="text-gray-900 dark:text-white underline hover:no-underline"
			on:click={click}
			data-md={data_md}
			data-id={data_id || ''}><strong><slot /></strong></A
		>
	{:else}
		<strong><slot /></strong>
	{/if}
</P>

<!-- <P class="max-w-xs"
	><InfoCircleOutline
		size="xs"
		class="inline"
		on:click={click}
		data-md={data_md}
		data-id={data_id}
	/> <strong><slot /></strong></P
> -->

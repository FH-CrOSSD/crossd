<script context="module" lang="ts">
	import type { overlayData } from '$lib/types';
	export let clickedSelector = writable();
	export let overlayStore = writable<overlayData|null>();
</script>

<script lang="ts">
	import { P } from 'flowbite-svelte';
	import { writable } from 'svelte/store';
	import MetricLabel from './MetricLabel.svelte';

	export let data_id: string|null;
	export let data_md: string|null;
	export let selector: Function;
	export let selected: number;
	// export let click: Function;
	export let chart: Boolean=false;
	// export let chart:Boolean;
	// export let overlayData;

	function clicked(event) {
		clickedSelector.set(selector);
		// click(event);
		overlayStore.set({
			current_id: data_id,
			current_md: data_md,
			definition: Boolean(data_md || false),
			chart:true
		});
		event.preventDefault();
	}
</script>

<MetricLabel click={clicked} {chart} {data_id} {data_md}><slot /></MetricLabel>
<slot name="value"/>

<script context="module" lang="ts">
	import type { overlayData } from '$lib/types';
	export let clickedSelector = writable();
	export let overlayStore = writable<overlayData | null>();
</script>

<script lang="ts">
	import { writable } from 'svelte/store';
	import MetricLabel from './MetricLabel.svelte';

	export let data_id: string | null = null;
	export let data_md: string | null = null;
	export let selector: Function;
	export let chart: Boolean = false;
	// handle click on value
	export let clicked = (event: Event) => {
		// hand the page the selector for the clicked value
		$clickedSelector = selector;
		// notify the page to show the metric definition and/or chart
		$overlayStore = {
			current_id: data_id,
			current_md: data_md,
			definition: Boolean(data_md || false),
			chart: chart
		};
		event.preventDefault();
	};
</script>

<MetricLabel click={clicked} {chart} {data_id} {data_md}><slot /></MetricLabel>
<slot name="value" />

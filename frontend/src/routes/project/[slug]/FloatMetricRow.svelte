<script lang="ts">
	import Row from './Row.svelte';
	import { P } from 'flowbite-svelte';
	import { toFixed2 } from '$lib/util';
	import MetricValue from './MetricValue.svelte';

	export let data_id: string | null;
	export let data_md: string | null;
	export let selector: Function;
	export let selected: number;
	export let chart: Boolean = false;
</script>

<Row {data_id} {data_md} {selector} {chart}>
	<slot />
	<svelte:fragment slot="value">
		<MetricValue value={toFixed2(selector(selected))} />
	</svelte:fragment>
</Row>

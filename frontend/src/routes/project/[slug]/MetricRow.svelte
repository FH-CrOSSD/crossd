<script lang="ts">
	import MetricValue from './MetricValue.svelte';
	import Row from './Row.svelte';
	import { P } from 'flowbite-svelte';

	export let data_id: string | null = null;
	export let data_md: string | null = null;
	export let selector: Function;
	export let selected: number;
	export let chart: Boolean = false;
</script>

<Row {data_id} {data_md} {selector} {chart}>
	<slot />
	<!-- <P slot="value" class="max-w-xs">{selector(selected)}</P> -->
	<svelte:fragment slot="value">
		<MetricValue value={selector(selected)} />
	</svelte:fragment>
</Row>

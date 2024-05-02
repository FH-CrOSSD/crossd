<script lang="ts">
	import MetricValue from './MetricValue.svelte';
	import Row from './Row.svelte';

	export let data_id: string | null = null;
	export let data_md: string | null = null;
	export let selector: Function;
	export let selected: number;
	export let chart: Boolean = false;
</script>

<Row {data_id} {data_md} {selector} {chart}>
	<slot />
	<svelte:fragment slot="value">
		<MetricValue value={selector(selected)} />
	</svelte:fragment>
</Row>

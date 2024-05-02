<script lang="ts">
	import { P } from 'flowbite-svelte';
	import Row from './Row.svelte';

	export let data_id: string | null = null;
	export let data_md: string | null = null;
	export let selector: Function;
	export let selected: number;
	export let chart: Boolean = false;
	export let iconFn: Function;
</script>

<Row {data_id} {data_md} {selector} {chart}>
	<slot />
	<P slot="value" class="max-w-xs"><svelte:component this={iconFn(selector(selected))} /></P>
</Row>

<script lang="ts">
	import Row from './Row.svelte';
	import { P } from 'flowbite-svelte';
	import Bool from '$lib/Bool.svelte';

	export let data_id: string | null;
	export let data_md: string | null;
	export let selector: Function;
	export let selected: number;
	export let chart: Boolean = false;
</script>

<Row {data_id} {data_md} {selector} {selected} {chart}>
	<slot />
	<!-- <P slot="value" class="max-w-xs">{selector(selected)}</P> -->
	<P slot="value" class="max-w-xs"><Bool value={selector(selected)} /></P>
</Row>

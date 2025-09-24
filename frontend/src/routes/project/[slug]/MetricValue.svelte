<script lang="ts">
	import { P } from 'flowbite-svelte';

	export let value: any;
	export let valueClass: string = '';
	$: mvalue = value?.toString() ?? '-';
</script>

<P class="max-w-28 {valueClass}">
	{mvalue}
</P>

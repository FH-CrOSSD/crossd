<script lang="ts">
	import { P } from 'flowbite-svelte';

	export let value: any;
	$: mvalue = value?.toString() ?? '-';
</script>

<P class="max-w-60">
	{mvalue}
</P>

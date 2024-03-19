<script lang="ts">
	export let value: boolean;
	import { CheckCircleSolid, XCircleSolid } from 'flowbite-svelte-icons';
</script>

<svelte:component
	this={value ? CheckCircleSolid : XCircleSolid}
	class={value ? 'text-lime-400' : 'text-red-400'}
/>

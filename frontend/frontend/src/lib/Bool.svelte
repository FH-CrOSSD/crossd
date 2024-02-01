<script lang="ts">
	export let value: boolean;
	import { CheckCircleSolid, CloseCircleSolid } from 'flowbite-svelte-icons';
</script>

<svelte:component
	this={value ? CheckCircleSolid : CloseCircleSolid}
	class={value ? 'text-lime-400' : 'text-red-400'}
/>

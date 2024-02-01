<script lang="ts">
	import '../app.pcss';
	import { Navbar, NavBrand, DarkMode, VideoPlaceholder, Video } from 'flowbite-svelte';

	import logo from '$lib/assets/logo.webp';
	import { page } from '$app/stores';
	const btnClass =
		'text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-lg p-2.5 fixed right-2 top-12  md:top-3 md:right-2 z-50';
</script>

<Navbar let:hidden let:toggle>
	<NavBrand href="/">
		<!-- <img src={logo} class="mr-3 h-6 sm:h-9" alt="Lorabridge Logo" /> -->
		<VideoPlaceholder size="sm" divClass="mr-3 h-6 sm:h-9" />
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
			CrOSSD
		</span>
	</NavBrand>
</Navbar>
<DarkMode {btnClass} />

<div class="mx-10">
<slot />
</div>

<style>
	:global(nav) {
		border-bottom-width: 2px;
		margin-bottom: 1em;
	}
</style>

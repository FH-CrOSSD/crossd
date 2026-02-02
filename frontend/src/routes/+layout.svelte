<script lang="ts">
	import {
		DarkMode,
		Footer,
		FooterCopyright,
		FooterIcon,
		FooterLink,
		FooterLinkGroup,
		NavBrand,
		NavLi,
		NavUl,
		Navbar
	} from 'flowbite-svelte';
	// import '../app.pcss';
	import '../app.css';
	import { onMount } from 'svelte';
	import { ArrowUpRightFromSquareOutline } from 'flowbite-svelte-icons';
	// import { theme } from '$lib/util';

	const btnClass =
		'text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-lg p-2.5 z-50';
	onMount(() => {
		if ('THEME_PREFERENCE_KEY' in localStorage) {
			// explicit preference - overrides author's choice
			localStorage.getItem('THEME_PREFERENCE_KEY') === 'dark'
				? window.document.documentElement.classList.add('dark')
				: window.document.documentElement.classList.remove('dark');
			// theme.set('dark');
		} else {
			// browser preference - does not overrides
			if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
				window.document.documentElement.classList.add('dark');
				// theme.set('dark');
			} 
			// else {
				// theme.set('light');
			// }
		}
	});
</script>

<Navbar
	class="bg-gray-50 dark:bg-gray-900 text-gray-700 dark:text-gray-200 border-gray-100 dark:border-gray-700 px-2 sm:px-4 py-2.5 w-full"
>
	<!-- navContainerClass="border-gray-100 dark:border-gray-700 divide-gray-100 dark:divide-gray-700" class="text-gray-700 dark:text-gray-200 dark:bg-gray-900 bg-white"> -->
	<NavBrand href="/">
		<span class="heading self-center whitespace-nowrap text-6xl font-semibold dark:text-white">
			CrOSSD
		</span>
	</NavBrand>
	<NavUl class="ml-auto">
		<NavLi href="/">Search</NavLi>
		<NavLi href="/groups">Groups</NavLi>
		<NavLi href="/doc">Metrics</NavLi>
		<NavLi href="https://fh-crossd.github.io/">Docs<ArrowUpRightFromSquareOutline class="inline h-4 mb-0.5" /></NavLi>
		<NavLi href="https://crossd.tech">Project & Blog<ArrowUpRightFromSquareOutline class="inline h-4 mb-0.5" /></NavLi>
	</NavUl>
	<!-- <DarkMode {btnClass} onclick={toggleMode} /> -->
	<DarkMode {btnClass}/>
</Navbar>
<div class="overflow-y-auto p-0 m-0 h-[calc(76vh))] min-h-fit">
<div class="container mx-auto my-10 ">
	<slot />
</div>
</div>
<Footer class="my-10 container mx-auto" footerType="undefined">
	<FooterCopyright href="/" by="University of Applied Sciences St. Pölten" year={2026} />
	<FooterLinkGroup
		class="flex flex-wrap items-center mt-3 text-sm text-gray-500 dark:text-gray-400 sm:mt-0"
	>
		<FooterLink href="/about">About Project</FooterLink>
		<FooterLink href="/privacy">Privacy Policy</FooterLink>
		<FooterLink href="/legal-information">Legal Information</FooterLink>
		<div class="ml-auto w-[10%]">
			<FooterIcon href="">
				<img
					class="visible dark:invisible dark:w-0 dark:h-0 pb-3"
					src="/netidee-logo-light.svg"
					alt="netidee logo"
				/>
				<img
					class="invisible w-0 h-0 dark:visible dark:w-auto dark:h-auto pb-3"
					src="/netidee-logo-dark.svg"
					alt="netidee logo"
				/>
			</FooterIcon>
		</div>
	</FooterLinkGroup>
</Footer>

<style>
		/* :global(:root) {
			color-scheme: light dark;
		} */
	:global(nav) {
		border-bottom-width: 2px;
		margin-bottom: 1em;
		border-color: light-dark(var(--color-gray-100), var(--color-gray-700));
	}
	:global(.light) {
		/* forces light color-scheme */
		color-scheme: light;
	}
	:global(.dark) {
		/* forces dark color-scheme */
		color-scheme: dark;
	}
	@font-face {
		font-family: Anta;
		src: url('/Anta-Regular.ttf');
	}
	.heading {
		font-family: 'Anta';
	}
	:global(div) {
		font-family: 'Anta';
	}
</style>

<script lang="ts">
	import '../app.pcss';
	import { Navbar, NavBrand, DarkMode, VideoPlaceholder, Video, NavUl,NavLi } from 'flowbite-svelte';
	import { Footer, FooterCopyright, FooterLinkGroup, FooterLink } from 'flowbite-svelte';
	// import logo from '$lib/assets/logo.webp';
	import { page } from '$app/stores';
	// const btnClass = 'text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-lg p-2.5 fixed right-2 top-12  md:top-3 md:right-2 z-50';
	const btnClass =
		'text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-lg p-2.5 z-50';
</script>
<Navbar>
	<NavBrand href="/">
		<!-- <img src={logo} class="mr-3 h-6 sm:h-9" alt="Lorabridge Logo" /> -->
		<!-- <VideoPlaceholders size="sm" divClass="mr-3 h-6 sm:h-9" /> -->
		<span class="heading self-center whitespace-nowrap text-6xl font-semibold dark:text-white">
			CrOSSD
		</span>
	</NavBrand>
	<NavUl class="ml-auto">
    <NavLi href="/">Home</NavLi>
    <NavLi href="/doc">Metrics</NavLi>
    <NavLi href="https://crossd.tech">Project & Blog</NavLi>
  </NavUl>
	<DarkMode {btnClass} />
</Navbar>
<div class="container mx-auto my-10">
	<slot />
</div>

<Footer class="sticky top-[100vh] my-10 container mx-auto">
	<FooterCopyright href="/" by="St. Pölten University of Applied Sciences" year={2024} />
	<FooterLinkGroup
		ulClass="flex flex-wrap items-center mt-3 text-sm text-gray-500 dark:text-gray-400 sm:mt-0"
	>
		<FooterLink href="https://crossd.tech/">About Project</FooterLink>
		<FooterLink href="/privacy">Privacy Policy</FooterLink>
		<FooterLink href="/legal-information">Legal Information</FooterLink>
		<!-- <FooterLink href="/">Licensing</FooterLink>
    <FooterLink href="/">Contact</FooterLink> -->
	</FooterLinkGroup>
</Footer>

<style>
	:global(nav) {
		border-bottom-width: 2px;
		margin-bottom: 1em;
	}
	@font-face {
		font-family: Anta;
		src: url('/Anta-Regular.ttf');
	}
	@font-face {
		font-family: Micro5;
		src: url('/Micro5-Regular.ttf');
	}
	@font-face {
		font-family: ProtestGuerrilla;
		src: url('/ProtestGuerrilla-Regular.ttf');
	}
	@font-face {
		font-family: ProtestRevolution;
		src: url('/ProtestRevolution-Regular.ttf');
	}
	@font-face {
		font-family: KodeMono;
		src: url('/KodeMono-VariableFont_wght.ttf');
	}
	.heading {
		font-family: 'Anta';
	}
	:global(div) {
		font-family: 'Anta';
	}
</style>

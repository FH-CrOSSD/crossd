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
// 	onMount(async () => {
// 		const pipe = await pipeline("text-generation", "HuggingFaceTB/SmolLM2-1.7B-Instruct");
// 		const out = await pipe(`
// 		Here are some metric definitions:
// Elephant Factor
// (CHAOSS, 2023)
// Description
// This metric expresses the distribution of contributions by the community across the companies the contributors belong to.
// Result
// Total number with the value 1 or higher, for instance an elephant factor of 2 means that more than 50% of the contributions are committed by 2 companies.
// Interpretation
// According to the provided definition6, a project with a low elephant factor may be more vulnerable to decisions by a small number of companies. The volume of contributions should be considered in the interpretation for a more reliable conclusion.

// Criticality Score
// (Arya, Brown, Pike, & Foundation, 2023)
// Description
// The project presenting this metric is maintained by member of the Securing Critical Projects WG4 and aims to detect critical projects, the open-source community depends on. The calculation includes various information about a repository, listed in the parameters below.
// Result
// The returned value is in the range of 0 to 100.
// Interpretation
// This metric represents a project's influence and importance. A high number implicates a high criticality, and therefore a high dependence of the OS community on the project.
// Maturity Level
// (Madaehoh & Senivongse, 2022)
// Description
// Considered as quality metric, this measure includes a repositories age, issues and releases. The issues and minor releases are counted and all values, including the age, are subdivided in group. Each group is represented by a score in the range of 0-5. For this metric, a low number of issues and a high number of minor releases and a higher age are considered positive.
// Result
// The returned score is a value in the range of 20 -- 100, whereas a higher score indicates a better quality then a lower score.
// Interpretation
// The returned level score represents the maturity. Regarding the parameters in this metric, the maturity refers to the development stage. For instance, a project in a late development stage with fewer issues, more releases and a higher age would result in a higher score than a project in an earlier stage.
// Support Rate
// (Madaehoh & Senivongse, 2022)
// Description
// The support rate refers to issues and pulls which received a response during the last 90 days. As responses are considered comments. This metric provides an insight into the support availability over a project's community. The formulas are implemented as recommended and documented below.
// Result
// The returned value is in the range of 0 to 100, a high value mirrors a high support rate.
// Interpretation
// A high support rate implies a high communication activity across the community and developers. Thus, this metric provides crucial insights into the support routine of developers and users.
// b. Custom GitHub community health percentage score (adapted)
// Result:
// A value between 0 and 100, representing the extent of existing documentation files.
// Interpretation:
// A high value represents a well-maintained documentation state of a project, with a higher information value than the adopted metric due to including all available documentation information. Can be compared to the origin health score for a validity check.


// Interpret the following metric values of a repository regarding the metric definition:
// Elephant factor:
// 4
// Maturity level:
// 73.33
// Criticality score:
// 72
// Support rate:
// 47.14	
// Github community healh:
// 100


// Provide me with a small summary with 5 sentences. Just the summary.

// 		`);
// 		console.log(out);
// 	})
// 	import { pipeline } from '@huggingface/transformers';
	
	// function toggleMode() {
	// 	document.documentElement.classList.toggle('dark');
	// 	localStorage.setItem(
	// 		'THEME_PREFERENCE_KEY',
	// 		localStorage.getItem('THEME_PREFERENCE_KEY') != 'dark' ? 'dark' : 'light'
	// 	);
	// 	theme.set(localStorage.getItem('THEME_PREFERENCE_KEY'));
	// }
</script>

<Navbar
	class="bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-200 border-gray-100 dark:border-gray-700 px-2 sm:px-4 py-2.5 w-full"
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
		<NavLi href="https://fh-crossd.github.io/">Docs</NavLi>
		<NavLi href="https://crossd.tech">Project & Blog</NavLi>
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
	<FooterCopyright href="/" by="St. Pölten University of Applied Sciences" year={2025} />
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
	:global(:root) {
		color-scheme: light dark;
	}
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

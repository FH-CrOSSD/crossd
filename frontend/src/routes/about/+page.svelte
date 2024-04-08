<script lang="ts">
	import { Heading, P } from 'flowbite-svelte';
</script>

<div class="mx-auto max-w-5xl">
	<Heading tag="h1" class="mb-5">About CrOSSD</Heading>
	<P class="mb-5"
		>The Critical Open-Source Software Database (CrOSSD) is an open-source software (OSS) project
		meant to assist a variety of stakeholders to make informed decisions about which OSS projects to
		use, assist or support.</P
	>
	<P class="mb-5"
		>By collecting and continuously monitoring a growing catalogue of OSS projects according to a
		selection of curated metrics, CrOSSD gives a comprehensive overview of the state of the observed
		projects: How stable are they? How often are they updated? How many active contributors are
		there? Do they come from different organisations? The answers to these questions (and more)
		allow lay users and software developers to decide which projects they want to include in their
		own codebase and which projects might benefit from their involvement and assistance as well as
		funding agencies or companies to allocate funding or support to critically important OSS
		projects in need of help.</P
	>
	<P class="mb-5">
		The current iteration of CrOSSD is based on a Kubernetes cluster consisting of various
		containers built upon Docker images. We utilise different Python crawlers to gather information
		about OSS repositories and calculate our set of metrics. Those results are stored inside an
		ArangoDB as JSON documents. The crawlers retrieve their tasks from a Celery task queue using
		Redis as a broker. The public interface for our cluster is web frontend built with Svelte and
		SvelteKit, which provides a search functionality and presents our metrics.
	</P>
	<P
		>We are regularly crawling selected sets of projects and recording their metrics. Currently, we
		are limiting our scope to projects publicly listed on GitHub, but we are actively developing it
		and continuously improving it. If you have suggestions for desirable features or wish to
		contribute yourself, please let us know!
	</P>
</div>

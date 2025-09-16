<script lang="ts">
	import { TabItem } from "flowbite-svelte";
	import Statistics from "./Statistics.svelte";

	let { title, activeClass, open = false } = $props();
</script>

<TabItem {open} {title} {activeClass}>
	<Statistics
		{...{
			name: data.name,
			count: test?.projects?.length,
			elephant_factor: group.data.avg.elephant_factor,
			maturity_level: group.data.avg.maturity_level,
			criticality_score: group.data.avg.criticality_score,
			support_rate: group.data.avg.support_rate,
			github_community_health_percentage: group.data.avg.github_community_health_percentage
		}}
	/>
</TabItem>

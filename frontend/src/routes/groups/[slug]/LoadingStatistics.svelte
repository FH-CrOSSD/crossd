<script lang="ts">
	import { Card, Heading, Skeleton, TabItem, Tabs, WidgetPlaceholder } from 'flowbite-svelte';
</script>

<Tabs style="underline" class="w-full" contentClass="bg-white dark:bg-gray-800">
	<TabItem open class="bg-white">
		{#snippet titleSlot()}
			<div class="mb-2.5 h-2.5 w-32 rounded-full bg-gray-200 dark:bg-gray-700 animate-pulse"></div>
		{/snippet}
		<div class="flex flex-wrap gap-10">
			<Card class="p-5">
				<Heading tag="h4" class="mb-5">Stats</Heading>
				<Skeleton size="sm" class="my-5"></Skeleton>
			</Card>
			<WidgetPlaceholder class="w-1/3" />
		</div>
	</TabItem>
	<TabItem class="bg-white" disabled>
		{#snippet titleSlot()}
			<div class="mb-2.5 h-2.5 w-32 rounded-full bg-gray-200 dark:bg-gray-700 animate-pulse"></div>
		{/snippet}
	</TabItem>
</Tabs>

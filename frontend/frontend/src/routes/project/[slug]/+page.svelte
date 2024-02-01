<script lang="ts">
	/** @type {import('./$types').PageData */
	export let data: { title: string; data: [{ [key: string]: any }]; bak: [{ [key: string]: any }] };
	let workflow_statuses: { [key: string]: any } = {};
	let project_id: string;
	$: {
		if (data.bak && data.bak.length >= 1) {
			project_id = Object.keys(data.bak[0]['elephant_factor'])[0];
		}
	}
	$: {
		workflow_statuses = {};
		for (const [key, value] of Object.entries(data.data[0]['current_state_workflows']) as [
			[string, { [key: string]: any }]
		]) {
			if (!(value['conclusion'] in workflow_statuses)) {
				workflow_statuses[value['conclusion']] = 1;
			} else {
				workflow_statuses[value['conclusion']]++;
			}
		}
		// console.log(workflow_statuses);
		// workflow_statuses["failure"]=1;
	}
	import { Alert, Button, Card, Hr } from 'flowbite-svelte';
	import { Heading, P, A, Mark, Secondary } from 'flowbite-svelte';
	import Bool from '$lib/Bool.svelte';

	import {
		CheckCircleSolid,
		CloseCircleSolid,
		ThumbsUpSolid,
		ThumbsDownSolid,
		QuestionCircleSolid
	} from 'flowbite-svelte-icons';
	function osiIcon(type: string) {
		switch (type) {
			case 'osi_approved':
				return ThumbsUpSolid;
			case 'not_osi_approved':
				return ThumbsDownSolid;
			case 'not_found':
				return QuestionCircleSolid;
		}
	}
</script>

<div class="p-8">
	<Heading tag="h1">{data.title}</Heading>
	<Hr />
	<!-- <div class="grid grid-flow-col auto-cols-fr auto-rows-auto gap-4"> -->
	<div class="flex flex-wrap gap-4">
		<Card size="lg">
			<div class="grid grid-cols-2 gap-y-4 gap-x-12 max-w-xl">
				<P><strong>Pull Requests (mean):</strong></P>
				<P>{data.data[0]['mean_pull_requests']}</P>
				<P><strong>Pull Requests (median):</strong></P>
				<P>{data.data[0]['median_pull_requests']}</P>
				<P><strong>Dependents:</strong></P>
				<P>{data.data[0]['dependents_count']}</P>
				<P><strong>Dependencies:</strong></P>
				<P>{data.data[0]['dependencyCount']}</P>
				<P><strong>Feature Requests:</strong></P>
				<P>{data.data[0]['feature_request_count']}</P>
				<P><strong>Closed Feature Requests:</strong></P>
				<P>{data.data[0]['closed_feature_request_count']}</P>
				<P><strong>Security Policy:</strong></P>
				<!-- <P>{data.data[0]['has_security_policy']}</P> -->
				<P><Bool value={data.data[0]['has_security_policy']} /></P>
				<P><strong>Contribution Policy:</strong></P>
				<P><Bool value={data.data[0]['has_contributing_policy']} /></P>
				<P><strong>Collaboration Platform:</strong></P>
				<P><Bool value={data.data[0]['has_collaboration_platform']} /></P>
				<P><strong>Fundable:</strong></P>
				<P><Bool value={data.data[0]['is_fundable']} /></P>
				<P><strong>Workflows:</strong></P>
				<P><Bool value={data.data[0]['uses_workflows']} /></P>
				{#if data.data[0]['uses_workflows']}
					<P><strong>Workflow Statuses:</strong></P>
					<P>
						{#each Object.entries(workflow_statuses) as status}
							{status[1]} {status[0]}<br />
						{/each}
					</P>
				{/if}

				<!-- {#each Object.entries(data.data[0]) as elem}
				{#if !elem[0].startsWith('_')}
					<P><strong>{elem[0]}:</strong></P>
					<P style="word-wrap:break-word"
						><span>
							{#if elem[1] === true}
								<CheckCircleSolid class="text-lime-400" />
							{:else if elem[1] === false}
								<CloseCircleSolid class="text-red-400" />
							{:else}
								{elem[1]}
							{/if}
						</span></P
					>
				{/if}
			{/each} -->
				<!-- <P>ads</P>
			<P style="word-wrap:break-word"
				><span
					>aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa</span
				></P> -->
			</div>
		</Card>
		<Card size="lg">
			<div class="grid grid-cols-2 gap-y-4 gap-x-12 max-w-xl">
				<P><strong>Elephant factor:</strong></P>
				<P>{data.bak[0]['elephant_factor'][project_id]}</P>
				<P><strong>Churn:</strong></P>
				<P>{data.bak[0]['churn'][project_id].toFixed(2)}</P>
				<P><strong>Community size:</strong></P>
				<P>{data.bak[0]['size_of_community'][project_id]}</P>
				<P><strong>Support contributors:</strong></P>
				<P>{data.bak[0]['number_of_support_contributors'][project_id]}</P>
				<P><strong>Maturity level:</strong></P>
				<P>{data.bak[0]['maturity_level'][project_id].toFixed(2)}</P>
				<P><strong>OSI approved license:</strong></P>
				<P>
					<svelte:component this={osiIcon(data.bak[0]['osi_approved_license'][project_id])} />
				</P>
				<P><strong>Criticality score:</strong></P>
				<P>{data.bak[0]['criticality_score'][project_id]}</P>
				<P><strong>Support rate:</strong></P>
				<P>{data.bak[0]['support_rate'][project_id].toFixed(2)}</P>
				<P><strong>Code dependency upstream:</strong></P>
				<P>{data.bak[0]['code_dependency'][project_id]['total_upstream']}</P>
				<P><strong>Code dependency downstream:</strong></P>
				<P>{data.bak[0]['code_dependency'][project_id]['total_downstream']}</P>
				<P><strong>Total forks:</strong></P>
				<P>{data.bak[0]['technical_fork'][project_id]['total_forks']}</P>
				<P><strong>Average forks per week:</strong></P>
				<P>{data.bak[0]['technical_fork'][project_id]['average_forks_created_per_week']}</P>
			</div>
		</Card>
		<Card size="lg">
			<Heading tag="h5" class="mb-4">Pull requests (PR)</Heading>
			<div class="grid grid-cols-2 gap-y-4 gap-x-12 max-w-xl">
				<P><strong>Total PR:</strong></P>
				<P>{data.bak[0]['pull_requests'][project_id]['total_pulls']}</P>
				<P><strong>Average days for closing PR:</strong></P>
				<P>{data.bak[0]['pull_requests'][project_id]['avg_pull_closing_days'].toFixed(2)}</P>
				<P><strong>Ratio open PR:</strong></P>
				<P>{data.bak[0]['pull_requests'][project_id]['ratio_open_total'].toFixed(2)}</P>
				<P><strong>Ratio closed PR:</strong></P>
				<P>{data.bak[0]['pull_requests'][project_id]['ratio_closed_total'].toFixed(2)}</P>
				<P><strong>Ratio merged PR:</strong></P>
				<P>{data.bak[0]['pull_requests'][project_id]['ratio_merged_total'].toFixed(2)}</P>
			</div>
		</Card>
		<Card size="lg">
			<Heading tag="h5" class="mb-4">Project velocity</Heading>
			<div class="grid grid-cols-2 gap-y-4 gap-x-12 max-w-xl">
				<P><strong>Total issues:</strong></P>
				<P>{data.bak[0]['project_velocity'][project_id]['total_issues']}</P>
				<P><strong>Closed issues:</strong></P>
				<P>{data.bak[0]['project_velocity'][project_id]['closed_issues']}</P>
				<P><strong>Open issues:</strong></P>
				<P>{data.bak[0]['project_velocity'][project_id]['open_issues']}</P>
				<P><strong>Pull count:</strong></P>
				<P>{data.bak[0]['project_velocity'][project_id]['pull_count']}</P>
				<P><strong>No pull count:</strong></P>
				<P>{data.bak[0]['project_velocity'][project_id]['no_pull_count']}</P>
				<P><strong>Ratio pull issue:</strong></P>
				<P>{data.bak[0]['project_velocity'][project_id]['ratio_pull_issue'].toFixed(2)}</P>
				<P><strong>Average days for resolving issue:</strong></P>
				<P>{data.bak[0]['project_velocity'][project_id]['avg_issue_resolving_days']}</P>
				<P><strong>Ratio open issues:</strong></P>
				<P>{data.bak[0]['project_velocity'][project_id]['ratio_open_total'].toFixed(2)}</P>
				<P><strong>Ratio closed issues:</strong></P>
				<P>{data.bak[0]['project_velocity'][project_id]['ratio_closed_total'].toFixed(2)}</P>
			</div>
		</Card>
		<Card size="lg">
			<Heading tag="h5" class="mb-4">Github community health</Heading>
			<div class="grid grid-cols-2 gap-y-4 gap-x-12 max-w-xl">
				<P><strong>Community Health score:</strong></P>
				<P
					>{data.bak[0]['github_community_health_percentage'][project_id][
						'community_health_score'
					]}</P
				>
				<P><strong>Custom Health score:</strong></P>
				<P>{data.bak[0]['github_community_health_percentage'][project_id]['custom_health_score']}</P
				>
				<!-- <P><strong>True count:</strong></P>
				<P>{data.bak[0]['github_community_health_percentage'][project_id]['true_count']}</P>
				<P><strong>False count:</strong></P>
				<P>{data.bak[0]['github_community_health_percentage'][project_id]['false_count']}</P> -->
				<P><strong>Has description:</strong></P>
				<P
					><Bool
						value={data.bak[0]['github_community_health_percentage'][project_id]['description']}
					/>
				</P>
				<P><strong>Has documentation:</strong></P>
				<P
					><Bool
						value={data.bak[0]['github_community_health_percentage'][project_id]['documentation']}
					/></P
				>
				<P><strong>Has code of conduct:</strong></P>
				<P
					><Bool
						value={data.bak[0]['github_community_health_percentage'][project_id]['code_of_conduct']}
					/></P
				>
				<P><strong>Has contributing:</strong></P>
				<P
					><Bool
						value={data.bak[0]['github_community_health_percentage'][project_id]['contributing']}
					/></P
				>
				<P><strong>Has issue templates:</strong></P>
				<P
					><Bool
						value={data.bak[0]['github_community_health_percentage'][project_id]['issue_template']}
					/></P
				>
				<P><strong>Has PR templates:</strong></P>
				<P
					><Bool
						value={data.bak[0]['github_community_health_percentage'][project_id][
							'pull_request_template'
						]}
					/></P
				>
				<P><strong>Has license:</strong></P>
				<P
					><Bool
						value={data.bak[0]['github_community_health_percentage'][project_id]['license']}
					/></P
				>
				<P><strong>Has README:</strong></P>
				<P
					><Bool
						value={data.bak[0]['github_community_health_percentage'][project_id]['readme']}
					/></P
				>
			</div>
		</Card>
		<Card size="lg">
			<Heading tag="h5" class="mb-4">Issues</Heading>
			<div class="grid grid-cols-2 gap-y-4 gap-x-12 max-w-xl">
				<P><strong>Total issues:</strong></P>
				<P>{data.bak[0]['issues'][project_id]['total_issues']}</P>
				<P><strong>Open issues:</strong></P>
				<P>{data.bak[0]['issues'][project_id]['open_issues']}</P>
				<P><strong>Closed issues:</strong></P>
				<P>{data.bak[0]['issues'][project_id]['closed_issues']}</P>
				<P><strong>New issues:</strong></P>
				<P>{data.bak[0]['issues'][project_id]['new_issues']}</P>
				<P><strong>Ratio new issues:</strong></P>
				<P>{data.bak[0]['issues'][project_id]['new_ratio']}</P>
				<P><strong>Average issues created per week:</strong></P>
				<P>{data.bak[0]['issues'][project_id]['average_issues_created_per_week']}</P>
				<P><strong>Average comments per issue:</strong></P>
				<P>{data.bak[0]['issues'][project_id]['average_issue_comments']}</P>
				<P><strong>Average days for resolving issues:</strong></P>
				<P>{data.bak[0]['issues'][project_id]['average_issue_resolving_days']}</P>
				<P><strong>Average days for first response:</strong></P>
				<P>{data.bak[0]['issues'][project_id]['average_first_response_time_days']}</P>
				<P><strong>Ratio open issues:</strong></P>
				<P>{data.bak[0]['issues'][project_id]['ratio_open_total'].toFixed(2)}</P>
				<P><strong>Ratio closed issues:</strong></P>
				<P>{data.bak[0]['issues'][project_id]['ratio_closed_total'].toFixed(2)}</P>
			</div>
		</Card>
		<Card size="lg">
			<Heading tag="h5" class="mb-4">Distribution of contributions</Heading>
			<div class="grid grid-cols-2 gap-y-4 gap-x-12 max-w-xl">
				<P><strong>Ratio of files tail:</strong></P>
				<P>{data.bak[0]['contributions_distributions'][project_id]['RoF_tail'].toFixed(2)}</P>
				<P><strong>Ratio of files dominant:</strong></P>
				<P>{data.bak[0]['contributions_distributions'][project_id]['RoF_dominant'].toFixed(2)}</P>
				<P><strong>Ratio of files diff percentage:</strong></P>
				<P
					>{data.bak[0]['contributions_distributions'][project_id]['RoF_diff_percent'].toFixed(
						2
					)}</P
				>
				<P><strong>Average contributors per file:</strong></P>
				<P
					>{data.bak[0]['contributions_distributions'][project_id][
						'avg_num_contributors_per_file'
					].toFixed(2)}</P
				>
				<P><strong>Bus factor score:</strong></P>
				<P>{data.bak[0]['contributions_distributions'][project_id]['bus_factor_score']}</P>
				<P><strong>Number of commits tail:</strong></P>
				<P>{data.bak[0]['contributions_distributions'][project_id]['NoC_tail'].toFixed(2)}</P>
				<P><strong>Number of commits dominant:</strong></P>
				<P>{data.bak[0]['contributions_distributions'][project_id]['NoC_dominant'].toFixed(2)}</P>
				<P><strong>Number of commits diff percentage:</strong></P>
				<P
					>{data.bak[0]['contributions_distributions'][project_id]['NoC_diff_percent'].toFixed(
						2
					)}</P
				>
			</div>
		</Card>
		<Card size="lg">
			<Heading tag="h5" class="mb-4">Lifecycle of branches</Heading>
			<div class="grid grid-cols-2 gap-y-4 gap-x-12 max-w-xl">
				<P><strong>Frequency of branch creation (days):</strong></P>
				<P>{data.bak[0]['branch_lifecycle'][project_id]['branch_creation_frequency_days']}</P>
				<P><strong>Average age of branches (days) :</strong></P>
				<P>{data.bak[0]['branch_lifecycle'][project_id]['branch_avg_age_days']}</P>
				<P><strong>Ratio stale branches:</strong></P>
				<P>{data.bak[0]['branch_lifecycle'][project_id]['stale_ratio']}</P>
				<P><strong>Ratio active branches:</strong></P>
				<P>{data.bak[0]['branch_lifecycle'][project_id]['active_ratio']}</P>
				<P><strong>Ratio unresolved branches:</strong></P>
				<P>{data.bak[0]['branch_lifecycle'][project_id]['unresolved_ratio']}</P>
				<P><strong>Ratio resolved branches:</strong></P>
				<P>{data.bak[0]['branch_lifecycle'][project_id]['resolved_ratio']}</P>
				<P><strong>Branch state counter:</strong></P>
				<P>{data.bak[0]['branch_lifecycle'][project_id]['branch_state_counter']}</P>
			</div>
		</Card>
		<Card size="lg">
			<Heading tag="h5" class="mb-4">Security advisories</Heading>
			<div class="grid grid-cols-2 gap-y-4 gap-x-12 max-w-xl">
				{#if Object.keys(data.bak[0]['security_advisories'][0][project_id]).length === 0}
					<P><strong>Advisories available:</strong></P>
					<P>No</P>
				{:else}
					<P><strong>Advisories available:</strong></P>
					<P
						>{data.bak[0]['security_advisories'][0][project_id]['advisories_available']
							? 'Yes'
							: 'No'}</P
					>
					<P><strong>Ratio patched:</strong></P>
					<P>{data.bak[0]['security_advisories'][0][project_id]['patch_ratio']}</P>
					<P><strong>Ratio closed:</strong></P>
					<P>{data.bak[0]['security_advisories'][0][project_id]['closed_advisories']}</P>
					<P><strong>Average CVSS score:</strong></P>
					<P>{data.bak[0]['security_advisories'][0][project_id]['average_cvss_score'].toFixed(2)}</P
					>
					<P><strong>Ratio high or critical severity:</strong></P>
					<P
						>{data.bak[0]['security_advisories'][0][project_id]['ratio_severity_high_crit'].toFixed(
							2
						)}</P
					>
				{/if}
			</div>
		</Card>
		<!-- "security_advisories": [
    {
      "304344049": {
        "advisories_available": true,
        "patch_ratio": 100,
        "closed_advisories": 0,
        "average_cvss_score": 7.166666666666667,
        "ratio_severity_high_crit": 66.66666666666666
      }
    },
    {
      "304344049": {
        "GHSA-g5m6-hxpp-fc49": {
          "cve_id": "CVE-2024-23641",
          "severity": "high",
          "state": "published",
          "published_at": "2024-01-24T00:24:51Z",
          "cvss_score": 7.5,
          "cwes": []
        },
        "GHSA-gv7g-x59x-wf8f": {
          "cve_id": "CVE-2023-29008",
          "severity": "medium",
          "state": "published",
          "published_at": "2023-04-06T16:24:08Z",
          "cvss_score": 4.7,
          "cwes": []
        },
        "GHSA-5p75-vc5g-8rv2": {
          "cve_id": "CVE-2023-29003",
          "severity": "critical",
          "state": "published",
          "published_at": "2023-04-04T18:07:26Z",
          "cvss_score": 9.3,
          "cwes": []
        }
      }
    }
  ], -->
	</div>
	<!-- <CheckCircleSolid class="text-lime-400" />
	<CloseCircleSolid class="text-red-400" /> -->
	<!-- {JSON.stringify(data.data)} -->
</div>

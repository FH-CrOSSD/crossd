import { error } from '@sveltejs/kit';



/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
    // const post = await getPostFromDatabase(params.slug);
    // do database stuff

    const post = { title: params.slug, data: b, bak: bak };


    if (post) {
        return post;
    }

    error(404, 'Not found');
}

let a = [
    {
        "_key": "6010382",
        "_id": "metrics/6010382",
        "_rev": "_hDhzbRm---",
        "mean_pull_requests": "5 days, 12:31:09.556018",
        "median_pull_requests": "18:20:16.500000",
        "dependents_count": 18,
        "has_security_policy": true,
        "dependencyCount": 0,
        "has_contributing_policy": false,
        "feature_request_count": 405,
        "closed_feature_request_count": 326,
        "has_collaboration_platform": true,
        "uses_workflows": true,
        "current_state_workflows": {
            "react-native-android-build-apk": {
                "created_at": "2023-12-11T12:33:21",
                "conclusion": "success"
            },
            "Build macOS M1": {
                "created_at": "2023-12-11T12:33:21",
                "conclusion": "success"
            },
            "Check pull request title": {
                "created_at": "2023-11-25T02:00:56",
                "conclusion": "success"
            },
            "CLA Assistant": {
                "created_at": "2023-12-11T12:32:52",
                "conclusion": "success"
            },
            "Close stale issues": {
                "created_at": "2023-12-06T16:02:40",
                "conclusion": "success"
            },
            "comment-on-failure": {
                "created_at": "2023-11-24T15:57:40",
                "conclusion": "success"
            },
            "Joplin Continuous Integration": {
                "created_at": "2023-12-11T12:33:21",
                "conclusion": "success"
            }
        },
        "is_fundable": true,
        "task_id": "918a50d7-3e54-4009-90e7-e012ce49c10f"
    }
];

let b = [
    {
        "_key": "6010040",
        "_id": "metrics/6010040",
        "_rev": "_hDzPS5i---",
        "mean_pull_requests": "5 days, 12:33:18.416257",
        "median_pull_requests": "18:21:38",
        "dependents_count": 18,
        "has_security_policy": true,
        "dependencyCount": 18734,
        "has_contributing_policy": false,
        "feature_request_count": 405,
        "closed_feature_request_count": 326,
        "has_collaboration_platform": true,
        "uses_workflows": true,
        "current_state_workflows": {
            "react-native-android-build-apk": {
                "created_at": "2023-12-12T00:07:46",
                "conclusion": "success"
            },
            "Build macOS M1": {
                "created_at": "2023-12-12T00:07:46",
                "conclusion": "success"
            },
            "Check pull request title": {
                "created_at": "2023-11-25T02:00:56",
                "conclusion": "success"
            },
            "CLA Assistant": {
                "created_at": "2023-12-12T00:07:46",
                "conclusion": "success"
            },
            "Close stale issues": {
                "created_at": "2023-12-07T16:02:21",
                "conclusion": "success"
            },
            "comment-on-failure": {
                "created_at": "2023-11-24T15:57:40",
                "conclusion": "success"
            },
            "Joplin Continuous Integration": {
                "created_at": "2023-12-12T00:07:46",
                "conclusion": "success"
            }
        },
        "is_fundable": true,
        "task_id": "9b607b21-18eb-4ee0-a8e7-1a93afbf1105"
    }
];

let bak = [{
    "_key": "475455755",
    "_id": "bak_metrics/475455755",
    "_rev": "_hTVT5vS--A",
    "maturity_level": {
        "79162682": 73.33333333333334
    },
    "osi_approved_license": {
        "79162682": "not_found"
    },
    "technical_fork": {
        "79162682": {
            "total_forks": 370,
            "average_forks_created_per_week": 14
        }
    },
    "criticality_score": {
        "79162682": 71
    },
    "pull_requests": {
        "79162682": {
            "total_pulls": 726,
            "avg_pull_closing_days": 2.4030874785591765,
            "ratio_open_total": 2.066115702479339,
            "ratio_closed_total": 97.93388429752066,
            "ratio_merged_total": 83.60881542699724
        }
    },
    "project_velocity": {
        "79162682": {
            "total_issues": 1479,
            "closed_issues": 1272,
            "open_issues": 207,
            "pull_count": 726,
            "no_pull_count": 753,
            "ratio_pull_issue": 49.08722109533469,
            "avg_issue_resolving_days": 42,
            "ratio_open_total": 13.995943204868155,
            "ratio_closed_total": 86.00405679513185
        }
    },
    "github_community_health_percentage": {
        "79162682": {
            "community_health_score": 71,
            "custom_health_score": 75,
            "true_count": 6,
            "false_count": 2,
            "description": true,
            "documentation": true,
            "code_of_conduct": false,
            "contributing": false,
            "issue_template": true,
            "pull_request_template": true,
            "license": true,
            "readme": true
        }
    },
    "issues": {
        "79162682": {
            "total_issues": 436,
            "open_issues": 155,
            "closed_issues": 281,
            "new_issues": 0,
            "new_ratio": 0,
            "average_issues_created_per_week": 1,
            "average_issue_comments": 5,
            "average_issue_resolving_days": 83,
            "average_first_response_time_days": 10,
            "ratio_open_total": 35.55045871559633,
            "ratio_closed_total": 64.44954128440367
        }
    },
    "support_rate": {
        "79162682": 6.447104357798166
    },
    "code_dependency": {
        "79162682": {
            "total_upstream": 5250,
            "total_downstream": 242
        }
    },
    // "security_advisories": [
    //     {
    //         "79162682": {}
    //     },
    //     {
    //         "79162682": {}
    //     }
    // ],
    "security_advisories": [
        {
            "79162682": {
                "advisories_available": true,
                "patch_ratio": 100,
                "closed_advisories": 0,
                "average_cvss_score": 7.166666666666667,
                "ratio_severity_high_crit": 66.66666666666666
            }
        },
        {
            "79162682": {
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
    ],
    "contributions_distributions": {
        "79162682": {
            "RoF_tail": 71.42857142857143,
            "RoF_dominant": 28.57142857142857,
            "RoF_diff_percent": 8.57142857142857,
            "avg_num_contributors_per_file": 1.07421875,
            "bus_factor_score": 2,
            "NoC_tail": 76.92307692307692,
            "NoC_dominant": 23.076923076923077,
            "NoC_diff_percent": 3.0769230769230766
        }
    },
    "number_of_support_contributors": {
        "79162682": 40
    },
    "size_of_community": {
        "79162682": 100
    },
    "churn": {
        "79162682": 30.983904465212873
    },
    "branch_lifecycle": {
        "79162682": {
            "branch_creation_frequency_days": 12,
            "branch_avg_age_days": 634,
            "stale_ratio": null,
            "active_ratio": null,
            "unresolved_ratio": null,
            "resolved_ratio": null,
            "branch_state_counter": {}
        }
    },
    "elephant_factor": {
        "79162682": 1
    },
    "task_id": "b057eaac-d194-4e41-be1c-3be329275404",
    "timestamp": 1706542100.2357514,
    "identity": {
        "name": "joplin",
        "owner": "laurent22",
        "name_with_owner": "laurent22/joplin"
    }
}];
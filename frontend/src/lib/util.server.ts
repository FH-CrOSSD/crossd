// import content of metric markdown files as string
import footnotes from '$lib/md/footnotes.md?raw';
import branches from '$lib/md/metric/branches.md?raw';
import change_pull_request from '$lib/md/metric/change_pull_request.md?raw';
import churn from '$lib/md/metric/churn.md?raw';
import code_dependencies from '$lib/md/metric/code_dependencies.md?raw';
import contributions_distributions from '$lib/md/metric/contributions_distributions.md?raw';
import criticality_score from '$lib/md/metric/criticality_score.md?raw';
import elephant_factor from '$lib/md/metric/elephant_factor.md?raw';
import github_community_health_percentage from '$lib/md/metric/github_community_health_percentage.md?raw';
import issues from '$lib/md/metric/issues.md?raw';
import maturity_level from '$lib/md/metric/maturity_level.md?raw';
import number_of_support_contributors from '$lib/md/metric/number_of_support_contributors.md?raw';
import osi_approved_licenses from '$lib/md/metric/osi_approved_licenses.md?raw';
import project_velocity from '$lib/md/metric/project_velocity.md?raw';
import security_advisories from '$lib/md/metric/security_advisories.md?raw';
import size_of_community from '$lib/md/metric/size_of_community.md?raw';
import support_rate from '$lib/md/metric/support_rate.md?raw';
import technical_fork from '$lib/md/metric/technical_fork.md?raw';

export const getMetricsMD = async () => {
    const res: { [key: string]: any } = {
        "branches.md": { text: branches },
        "change_pull_request.md": { text: change_pull_request },
        "churn.md": { text: churn },
        "code_dependencies.md": { text: code_dependencies },
        "contributions_distributions.md": { text: contributions_distributions },
        "criticality_score.md": { text: criticality_score },
        "elephant_factor.md": { text: elephant_factor },
        "github_community_health_percentage.md": { text: github_community_health_percentage },
        "issues.md": { text: issues },
        "maturity_level.md": { text: maturity_level },
        "number_of_support_contributors.md": { text: number_of_support_contributors },
        "osi_approved_licenses.md": { text: osi_approved_licenses },
        "project_velocity.md": { text: project_velocity },
        "security_advisories.md": { text: security_advisories },
        "size_of_community.md": { text: size_of_community },
        "support_rate.md": { text: support_rate },
        "technical_fork.md": { text: technical_fork }
    };

    return { metrics: res, footnotes: { text: footnotes } };
};
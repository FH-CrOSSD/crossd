# Criticality Score 
>(Arya, Brown, Pike, & Foundation, 2023)

## Description

The project presenting this metric is maintained by member of the
Securing Critical Projects WG[^4] and aims to detect critical projects,
the open-source community depends on. The calculation includes various
information about a repository, listed in the parameters below.

## Result

The returned value is in the range of 0 to 100.

## Interpretation

This metric represents a project's influence and importance. A high
number implicates a high criticality, and therefore a high dependence of
the OS community on the project.

## Limitations

The weights are adopted as documented, testing different values exceeds
the scope of this thesis.

## Parameters

$created\_since$ age in months.

$updated\_since$ time since last changes in months.

$contributors\_count$ Number of distinct contributors with
contributions.

$org\_count$ Number of distinct organizations, contributors belong to.

$commit\_frequency$ Frequency of commits which have been updated in the
last year.

$recent\_releases\_count$ Number of releases from the last year

$closed\_issues\_count$ Number of issues which have been closed in the
last 90 days.

$updated\_issues\_count$ Number of issues which have been updated in the
last 90 days.

$comment\_frequency$ Average number of comments in the last 90 days per
issue.

$dependents\_count$ Number of dependent projects according to the
dependency graph.

## Formula

The formula, including weight and max threshold values, is based on the
algorithm by Rob Pike[^5] described in the GitHub Project
criticality\_score (Arya, Brown, Pike, & Foundation, 2023).

$$C_{\text{proj}} = \ \frac{1}{\sum_{i}^{}a_{i}}\sum_{i}^{}a_{i}\frac{log(1 + S_{i})}{log(1 + max(S_{i},T_{i}))} \times 100$$

$S_{i}$ = Parameter

$\alpha_{i}$ = Weight

$T_{i}$ = Max threshold

## Adaptions

All parameters are adapted as documented in the project except the
dependents\_count, which is calculated by the dependents gathered from
GitHub's Dependency Graph instead of checking for mentions of the
concerned project in commit messages. Since the project's description
mentions, that the dependents are to be retrieved from the dependency
tree in future implementations, the gathering from the dependency graph
is a more accurate method then searching for the project's name through
commit messages.

Further the result is multiplicated to represent a more intuitive
value and for consistency across all metrics.

## Implementation

Except for the dependents, all data was gathered by the GitHub API. The
dependents displayed in a project's dependency graph are not available
via the API, thus they are scraped from the project website itself. For
performance reasons, only the top 100 issues are included for querying
concerning comments. Due to high computation costs the organizations are
only queried for the top 20% of the contributors with the most
contributions.

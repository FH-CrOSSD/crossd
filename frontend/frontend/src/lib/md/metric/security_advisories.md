# Security Advisories 
>(Unpatched CVE statistics (Tan, et al., 2022))

## Description

This metric is based on the aim of (Tan, et al., 2022) to better
understand security patches across branches. Following metrics exclude
an analysis across branches due to

feasibility reasons. As security risks are considered GitHub security
advisories which include CVEs. As (Tan, et al., 2022) includes a
comparison of the number of unpatched CVEs and the

CVSS score, these statistics are considered in the proposed metrics
below.

## Parameters

$$A_{i} = \{ i,\ i = \ \text{GitHub}\ \text{security}\ \text{advisory}\}$$

$$V_{i} = \{ i,\ i = \ \text{Advisory}\}$$

$$P_{i} = \{ i,\ i = \ \text{Patched}\ \text{advisories}\}$$

$$U_{i} = \{ i,\ i = \ \text{Unpatched}\ \text{advisories}\}$$

$$H_{i} = \{ i,\ i = \ \text{Advisories}\ \text{with}\ a\ \text{high}\ \text{or}\ \text{critical}\ \text{severity}\}$$

$$C_{i} = \{ i,\ i = \ \text{Advisories}\ \text{with}\ \text{state}\ \text{closed}\}$$

$$S_{i} = \{ i,\ i = \ \text{CVSS}\ \text{score}\ \text{per}\ \text{advisory}\}$$

## Submetrics

+----------------------------------------------------------------------------------------------------------------+
| ### a.  **Average CVSS Score** (adopted)                                                                       |
+================================================================================================================+
| #### **Result**:                                                                                               |
|                                                                                                                |
| Average over all CVSS scores of a repository.                                                                  |
+----------------------------------------------------------------------------------------------------------------+
| #### **Interpretation**:                                                                                       |
|                                                                                                                |
| Provides a summary of all CVSS scores in one value.                                                            |
+----------------------------------------------------------------------------------------------------------------+
| #### **Formula**:                                                                                              |
|                                                                                                                |
| $average\_ cvss\_ score = (\sum_{}^{}S_{i})/n(S)$                                                              |
+----------------------------------------------------------------------------------------------------------------+
| ### b.  **Existing advisories (created)**                                                                      |
+----------------------------------------------------------------------------------------------------------------+
| #### **Result**:                                                                                               |
|                                                                                                                |
| Returns a Boolean value which represents the existence of any                                                  |
| advisories. The result is 1 if advisories exist, and 0 if no                                                   |
| advisories exist.                                                                                              |
+----------------------------------------------------------------------------------------------------------------+
| #### **Interpretation**:                                                                                       |
|                                                                                                                |
| Since the other metrics require advisories, this information is                                                |
| utilized to compare the availability across all projects.                                                      |
+----------------------------------------------------------------------------------------------------------------+
| #### **Formula**:                                                                                              |
|                                                                                                                |
| $advisories\_ available = \left\{ \begin{matrix}                                                               |
| 1,\ \&\ \ n(A)\  > \ 0\ \ \ \ \ \ \  \\                                                                        |
| 0,\ \ otherwise \\                                                                                             |
| \end{matrix} \right.\ $                                                                                        |
+----------------------------------------------------------------------------------------------------------------+
| ### c.  **Patched advisories to total advisories ratio (created)**                                             |
+----------------------------------------------------------------------------------------------------------------+
| #### **Result**:                                                                                               |
|                                                                                                                |
| Returns a value between 0 and 100, representing the percentage of                                              |
| patched advisories.                                                                                            |
+----------------------------------------------------------------------------------------------------------------+
| #### **Interpretation**:                                                                                       |
|                                                                                                                |
| A high ratio indicates a well-maintained project with less security                                            |
| threats.                                                                                                       |
+----------------------------------------------------------------------------------------------------------------+
| #### **Formula**:                                                                                              |
|                                                                                                                |
| $patch\_ ratio\  = \ n(P)\ /\ n(V) \times 100$                                                                 |
+----------------------------------------------------------------------------------------------------------------+
| ### d.  **Number of closed advisories (created)**                                                              |
+----------------------------------------------------------------------------------------------------------------+
| #### **Result**:                                                                                               |
|                                                                                                                |
| Total number of advisories with the state "closed".                                                            |
+----------------------------------------------------------------------------------------------------------------+
| #### **Interpretation**:                                                                                       |
|                                                                                                                |
| Gives an insight into how many advisories have been closed in a                                                |
| certain project. Closed advisories may not be resolved, thus a                                                 |
| comparison with patched advisories provide more information.                                                   |
+----------------------------------------------------------------------------------------------------------------+
| #### **Formula**:                                                                                              |
|                                                                                                                |
| $closed\_ advisories\  = \ n(C)\ $                                                                             |
+----------------------------------------------------------------------------------------------------------------+
| ### e.  **Advisories with critical or high severity to total advisories ratio (created)**                      |
|                                                                                                                |
+----------------------------------------------------------------------------------------------------------------+
| #### **Result**:                                                                                               |
|                                                                                                                |
| Returns the percentage of advisories with a severity of high or                                                |
| critical in the range of 0 to 100.                                                                             |
+----------------------------------------------------------------------------------------------------------------+
| #### **Interpretation**:                                                                                       |
|                                                                                                                |
| To understand the total severity of advisories from a project, this                                            |
| metric aims to return the risk of security threats as OSS with most                                            |
| advisories with high or critical severity is more unsecure to use.                                             |
+----------------------------------------------------------------------------------------------------------------+
| #### **Formula**:                                                                                              |
|                                                                                                                |
| $patch\_ ratio\  = \ n(P)\ /\ n(V) \times 100\ $                                                               |
+----------------------------------------------------------------------------------------------------------------+

## Limitations

As mentioned, the advisories are not compared across a project's
different branches. A comparison across branches and versions may
provide insights into a project's development process concerning
vulnerability handling.

## Adaptions

Based on (Tan, et al., 2022) available information is either adopted or
new metrics are defined.

## Implementation

Since the implementation of a matching of CVEs to project branches is
out of the scope from this thesis due to no reliable state of the art
methods, GitHub's security advisory[^13] database is utilized. This data
source includes CVEs and corresponding information about the state,
severity, published date and the CVSS score (Common Vulnerability
Scoring System). The score is not available for each advisory, therefore
the CVE id is used to map the advisory to the related CVE from NVD to
retrieve the score from there. As patched vulnerabilities are considered
advisories with assigned patched code versions.

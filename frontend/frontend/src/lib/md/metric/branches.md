# Branches 
>(Branch Lifecycle (CHAOSS, 2023))

## Description
The following metrics are based on the branch
lifecycle[^16], instead of the lifecycle the overall branch development
is summarized. GitHub differs from active and stale branches, depending
on the last activity. A branch is considered as stale, when no commits
have been made in the last 120 days. Since there are more states then
open and closed, all states are grouped into resolved and unresolved.
Resolved includes branches with the state closed and merged and
unresolved includes branches with the state open and compare
respectively.

## Parameters

$$C_{i} = \{ i,i = Creation\ date\ per\ branch\}$$

$${T_{i} = \{ i,i = Day\ diff\ between\ each\ branch\ and
}{following\ branch\}}$$

$$D_{i} = \{ i,i = Age\ per\ branch\ in\ days\}$$

$$S_{i} = \{ i,i = Stale\ branches\}$$

$$A_{i} = \{ i,i = Active\ branches\}$$

$$M_{i} = \{ i,i = Branches\ with\ state\ merged\}$$

$$O_{i} = \{ i,i = Branches\ with\ state\ compare\}$$

$$P_{i} = \{ i,i = Branches\ with\ state\ open\}$$

$$L_{i} = \{ i,i = Branches\ with\ state\ closed\}$$

$$N = \{ O \cup P\}$$

## Submetrics

+----------------------------------------------------------------------+
| ### a.  **Total number of branches per state** (adopted)             |
+======================================================================+
| #### **Result**:                                                     |
|                                                                      |
| Total number of branches per state, including the states open,       |
| merged, deleted and compare.                                         |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| Provides an insight into the current state of all branches and the   |
| distribution of merged or deleted to open and in progress branches.  |
| Total numbers can be compared with other repositories of same size   |
| or can be analyzed combined with other sub metrics.                  |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $f(x)\  = \ n(x)$                                                    |
+----------------------------------------------------------------------+
| ### b.  **Average branch age (adopted)**                             |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Total number of average branch age in days of all branches which are |
| not assigned to the state closed or merged. The remaining branches   |
| are considered as open.                                              |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A long average resolving time indicates a slower project velocity.   |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$branch\_ avg\_ age\_ days = (\sum_{}^{}N_{i})/n(N)$$               |
+----------------------------------------------------------------------+
| ### c.  **Resolved branch to total branch ratio** (adapted)          |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Percentage of branches with the state merged or deleted in relation  |
| to all branches, returns a value between 0 and 100.                  |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| High portion of resolved branches imply a fast project development   |
| velocity.                                                            |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$resolved\_ ratio = (n(\{ M \cup L\})/n(C))\  \times 100$$          |
+----------------------------------------------------------------------+
| ### d.  **Unresolved branch to total branch ratio** (adapted)        |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Percentage of branches with the state open or compare in relation to |
| all branches, returns a value between 0 and 100.                     |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| High portion of unresolved branches imply a slow project development |
| velocity and pose the risk of the project to stall.                  |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$unresolved\_ ratio = (n(\{ P \cup O\})/n(C))\  \times 100$$        |
+----------------------------------------------------------------------+
| ### e.  **Branch creation frequency** (created)                      |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Average time difference in days between the creation of branches in  |
| a total number.                                                      |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| Low number indicates a fast development speed.                       |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$branch\_ creation\_ frequency\_ days = (\sum_{}^{}T_{i})/n(T)$$    |
+----------------------------------------------------------------------+
| ### f.  **Stale branch to total branch ratio** (created)             |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Percentage of stale branches to total branches in the range of 0 to  |
| 100.                                                                 |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| An exceptional high ratio of stale branches represents a stalling    |
| project, since the progress is low.                                  |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$stale\_ ratio = (n(S)/n(C))\  \times 100$$                         |
+----------------------------------------------------------------------+
| ### g.  **Active branch to total branch ratio** (created)            |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Percentage of active branches to total branches in the range of 0 to |
| 100.                                                                 |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A large number implies fast progress and an active contributing      |
| community.                                                           |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$stale\_ active = (n(A)/n(C))\  \times 100$$                        |
+----------------------------------------------------------------------+

## Limitations
Since no analysis over time is conducted, the progress
of branches over time is excluded. Additionally, the GitHub API provided
only minimal information about project branches.

## Adaptions
The grouping to resolved and unresolved is added to avoid
to many metrics and gain more information value.

## Implementation
Since GitHub's project websites include far more
information about branches then the API, such as the states and the
activity evaluation, this data is gathered by a web scraper. The
branches are additionally gathered by the API's endpoint, for the
large-scale sample only the top 100 branches are included due to
performance costs. The sample for the from related studies selected
repositories includes the top 999 branches.

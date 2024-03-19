# Project Velocity 
>(CHAOSS, 2023)

## Description

Velocity refers to the development speed of an organization or in this
thesis of GitHub repositories. (CHAOSS, 2023) includes in the
description of this metric[^7] the information to determine a
project's velocity, including the number of issues and pull requests,
volume commits and the number of contributors. Further, the number of
total and closed issues are mentioned and included in this metric.
Since no specific formula is presented which combines the mentioned
information and commits and contributors are already included in other
metrics, this metric is limited to the number of issues and pull
requests. Whereas in the metrics Change/Pull Requests and Issues the
information is limited to each data, this metric combines both
attributes. Thus, following scores are calculated with issues and pull
requests, since GitHub issues include pull request as issue objects.

## Parameters

$I_{i} = \ \{ i,\ i\ is\ created\ issue\ including\ pull\ requests\}$

$C_{i} = \ \{ i,\ i\ is\ closed\ issue\ including\ pull\ requests\}$

$O_{i} = \ \{ i,\ i\ is\ open\ issue\ including\ pull\ request\}$

$P_{i} = \ \{ i,\ i\ is\ issue\ with\ pull\ request\ id\}$

$N_{i} = \ \{ i,\ i\ is\ issue\ with\ no\ pull\ request\ id\}$

## Submetrics

+----------------------------------------------------------------------+
| ### a.  **Number of total issues** (adopted)                         |
+======================================================================+
| #### **Result**:                                                     |
|                                                                      |
| Total Number of all issues, including pull requests.                 |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| The number of total issues represents the number of objects waiting  |
| to be solved or reviewed. A large number reflects the activity of    |
| the community and contributors and on the other hand may represent   |
| the risk of the project to stall or leave issues unsolved.           |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$total\_ issues\  = \ n(I)$$                                        |
+----------------------------------------------------------------------+
| ### b.  **Number of closed issues** (adopted)                        |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Total number of all closed issues, including pull requests.          |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A high number can result from a low frequency of opened issues or a  |
| high activity of the reviewers, thus the value represents an         |
| indicator for a project's contributor and reviewer activity.\        |
| It is recommended to compare the result with either different time   |
| periods or other projects with a similar size and popularity or to   |
| combine it with other project information.                           |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$closed\_ issues\  = \ n(C)$$                                       |
+----------------------------------------------------------------------+
| ### c.  **Number of open issues** (created)                          |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Total number of all open and unresolved issues, including pull       |
| requests.                                                            |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| Opposing to the number of closed issues, this value indicates a      |
| project's inactivity of reviews or a high activity of contributors   |
| which are opening issues. Due to different interpretations a         |
| combination with other information or a comparison as mentioned in   |
| the number of closed issues metric is recommended.                   |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$closed\_ issues\  = \ n(O)$$                                       |
+----------------------------------------------------------------------+
| ### d.  **Number of total pull requests in issues** (created)        |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Number of total pull requests included in issues.                    |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| The number of pull requests represent the code change activity,      |
| information is recommended to be compared with other projects or     |
| combined with further information to draw a conclusion.              |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$pull\_ count\  = \ n(P)$$                                          |
+----------------------------------------------------------------------+
| ### e. **Number of total issues which are no pull request** (created)|
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Number of total pull requests included in issues.                    |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| The number of issues represent the code change activity, information |
| is recommended to be compared with other projects or combined with   |
| further information to draw a conclusion.                            |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$no\_ pull\_ count\  = \ n(N)$$                                     |
+----------------------------------------------------------------------+
| ### f.  **Number Pull request to total issues ratio** (created)      |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| A value between 0 and 100, the higher the result, the more pull      |
| requests in relation to issues are created.                          |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A high ratio means that more pull requests are created than issues   |
| are proposed, indicating that the code development progress prevails |
| over the activities reviewing and testing the code changes. The      |
| project development velocity may be to high, leaving not enough time |
| for the progress to be evaluated.\                                   |
| A low ratio can result from erroneous code, prone to raise a large   |
| number of issues and slowing down or stalling the project's          |
| development.                                                         |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$ratio\_ pull\_ issue\  = \ n(P)\ /\ n(I) \times 100$$              |
+----------------------------------------------------------------------+
| ### g.  **Average issue closing time** (created)                     |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Average number of days required to close an issue.                   |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A low result shows a high responsivity on created issues, a higher   |
| result value represents long response times indicating a slow        |
| project velocity and in the worst case the risk of a project stall.  |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$A_{d} = \{ d,d                                                     |
|  = Difference\ of\ creation\ and\ closing\ of\ an\ issue\ in\ days\} |
| $$                                                                   |
+----------------------------------------------------------------------+
| ### h.  **Open issues to total issues ratio** (created)              |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Returns a value between 0 and 100, a high ratio represents a large   |
| number of open issues compared to all issues.                        |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A high percentage of open issues can indicate a slow reviewing       |
| process or an active testing frequency by the community and          |
| contributors. For more information value, this metric is recommended |
| to be combined with other information.                               |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$ratio\_ open\_ total\  = \ n(O)\ /\ n(I) \times 100$$              |
+----------------------------------------------------------------------+
| ### i.  **Closed issues to total issues ratio** (created)            |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Returns a value between 0 and 100, a high ratio represents a large   |
| number of closed issues compared to all issues.                      |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| If the closed issue ratio is high, it can imply either a fast review |
| process or a low number of opened issues. Thus, this metric is       |
| recommended to be combined with other information.                   |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$\ ratio\_ closed\_ total\  = \ n(C)\ /\ n(I) \times 100$$          |
+----------------------------------------------------------------------+

## Limitations

The listed metrics are basic project information and would provide a
higher information value if they are either compared with historical
data per project or with other projects of similar size and popularity.

Further, the data could be expanded with reviewers per issue and the
volume of code changes. Due to feasibility, such analysis is excluded
from this thesis.

## Adaptions

As mentioned, information about the commits and contributors are
excluded.

## Implementation

The GitHub API request for all issues includes issues with all states.
The issues and pull requests are filtered for a period of 6 months.

# Issues 
> (New, Closed, Active) (CHAOSS, 2023)

## Description

Issues can be viewed from different perspectives, CHAOSS (CHAOSS, 2023)
differs issues by the categories new[^9], closed[^10] and active[^11]
respectively. New issues refer to created and reopened issues, active
issues to those which received comments or state changes and closed
issues are issues which have been resolved or closed.

The issues endpoint of the GitHub API includes issues and pulls, for
following metrics pull requests are excluded as they are already
included in other metrics such as the project velocity and change/pull
requests. The queried issues are to only include those which were
updated the last 90 days. Since a project's activity can increase and
decrease rather fast, a more recent picture is aimed for in following
metrics.

## Parameters

$I_{i} = \ \{ i,\ i\ \text{is}\ \text{issue}\}$

$N_{i} = \ \{ i,\ i\ \text{is}\ \text{created}\ \text{issue}\}$

$O_{i} = \ \{ i,\ i\ \text{is}\ \text{open}\ \text{issue}\}$

$C_{i} = \ \{ i,\ i\ \text{is}\ \text{closed}\ \text{issue}\}$

## Submetrics

+----------------------------------------------------------------------+
| ### a.  **Number of new/created issues** (adopted)                   |
+======================================================================+
| #### **Result**                                                      |
|                                                                      |
| Total number of issues which have been created in a certain time     |
| period.                                                              |
+----------------------------------------------------------------------+
| #### **Interpretation:**                                             |
|                                                                      |
| High number of created issues indicates an active community and      |
| contributors.                                                        |
+----------------------------------------------------------------------+
| #### **Formula:**                                                    |
|                                                                      |
| $$new\_ issues\  = \ n(N)$$                                          |
+----------------------------------------------------------------------+
| ### b.  **New issues to total issues ratio (adopted)**               |
+----------------------------------------------------------------------+
| #### **Result**<span class="underline">:</span>                      |
|                                                                      |
| Returns a value between 0 and 100, representing the percentage of    |
| new created issues in a time period in relation to all updated       |
| issues.                                                              |
+----------------------------------------------------------------------+
| #### **Interpretation:**                                             |
|                                                                      |
| A low ratio indicates that the project is more likely to stick to    |
| older issues, whereas a higher ratio implies an active contributing  |
| community.                                                           |
+----------------------------------------------------------------------+
| #### **Formula:**                                                    |
|                                                                      |
| $$new\_ ratio\  = \ n(N)\ /\ n(I) \times 100$$                       |
+----------------------------------------------------------------------+
| ### c.  **Number of closed issues** (adopted)                        |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Total number of issues which have been closed in a certain time      |
| period.                                                              |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A high number of closed issues represents a fast issue reviewing     |
| process.                                                             |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$closed\_ issues\  = \ n(C)$$                                       |
+----------------------------------------------------------------------+
| ### d.  **Closed issues to total issues ratio** (adopted)            |
+----------------------------------------------------------------------+
| #### **Result**<span class="underline">:</span>                      |
|                                                                      |
| Returns a value between 0 and 100, representing the percentage of    |
| closed issues to all updated issues in a certain time period.        |
+----------------------------------------------------------------------+
| #### **Interpretation:**                                             |
|                                                                      |
| A high ratio emphasizes a project's development and reviewing speed  |
+----------------------------------------------------------------------+
| #### **Formula:**                                                    |
|                                                                      |
| $$ratio\_ closed\_ total\  = \ n(C)\ /\ \ n(I) \times 100$$          |
+----------------------------------------------------------------------+
| ### e.  **Number of total issues** (created)                         |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Total number of issues which were updated in the selected time       |
| period.                                                              |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A high number of issues reflects an active community and can be      |
| compared with other projects with similar size and popularity.       |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $total\_ issues\  = \ n(I)$                                          |
+----------------------------------------------------------------------+
| ### f.  **Number of open issues** (created)                          |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Total number of open issues which were updated in a certain time     |
| period.                                                              |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A high number of open issues indicates that there are not enough     |
| project owners and contributors to review the issues in an           |
| appropriate time span. Absolute number can be compared like the      |
| number of total issues.                                              |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $open\_ issues\  = \ n(O)$                                           |
+----------------------------------------------------------------------+
| ### g.  **Open issues to total issues ratio** (created)              |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Returns the percentage of open issues as a value between 0 and 100.  |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| As in the number of open issues' interpretation mentioned, the       |
| inability to review issues in an appropriate time span can cause the |
| project to stall. Thus, a high ratio can be interpreted as risk,     |
| even if it indicates an active community as well.                    |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $ratio\_ open\_ total\  = \ n(O)\ /\ n(I) \times 100$                |
+----------------------------------------------------------------------+
| ### h.  **Average issues created per week** (created)                |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Average number of created issues per week in total.                  |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A large number mirrors an active and attentive community.            |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $A_{i} = \{ i,i = Number\ of\ issues\ created\ per\ each\ week\}$    |
|                                                                      |
| $average\_ issue\_ created\_ per\_ week = \left\lbrack \left         |
| ( \sum_{}^{}A_{i} \right)\text{/}n\left( A \right) \right\rbrack$*   |
|                                                                      |
| *$\text{Let\ }\left                                                  |
| \lbrack x \right\rbrack\text{\ mean\ the\ integer\ closest\ to\ x}$  |
+----------------------------------------------------------------------+
| ### i.  **Average issue comments** (created)                         |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Average number of comments with available id per issue in total.     |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| This metric mirrors the communication activity across issues, a high |
| average value means the contributors are eager to solve issues.      |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $A_{i} = \{ i,i = Number\ of\ comments\ per\ issue\}$                |
|                                                                      |
| $average\_ issue\_ comments = \left\lbrack \left                     |
| ( \sum_{}^{}A_{i} \right)\text{/}n\left( A \right) \right\rbrack$*   |
|                                                                      |
| *$\text{Let\ }\left                                                  |
| \lbrack x \right\rbrack\text{\ mean\ the\ integer\ closest\ to\ x}$  |
+----------------------------------------------------------------------+
| ### j.  **Average issue resolving days** (created)                   |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Average number of days required to change an issue's state from open |
| to closed in total.                                                  |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A low number is an indicator for a fast review process and moreover  |
| for a fast project velocity if the issues are resolved successfully. |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$A_{i} = \{ i,i = Difference\ of\ created\_ at\ and\ closed\_ at\}  |
| $$                                                                   |
+----------------------------------------------------------------------+
| ### k.  **Average first response time in days** (created)            |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Average number of days until a created issue received a first        |
| response in total.                                                   |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A fast first response represents a higher communication quality and  |
| review activity of a project, a large delay can indicate slow        |
| development and indicate to a not sufficiently maintained project.   |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| ${A_{i} = \{ i,i = Difference\ of\ created\_ at\ from\ issue\ and\   |
| }\\{created\_ at\ from\ first\ comment\                              |
| }{per\ issue\ with\ response\}                                       |
| }$                                                                   |
+----------------------------------------------------------------------+

## Limitations

For more information value is recommended to enrich the data with data
of contributors. Further, active issues can be detected by various
attributes. Possibly reopened issues are not considered in the proposed
metrics either. These possibilities are out of scope in this thesis due
to feasibility.

## Adaptions

CHAOSS (CHAOSS, 2023) proposes implementations with the ability to
select certain time periods. For this metrics, the issues are filtered
after their last updated timestamp to gain an accurate picture of the
recent state the projects are in.

## Implementation

As mentioned in the description, the issues are filtered by their
"updated\_at" timestamp respectively for the issues metrics.

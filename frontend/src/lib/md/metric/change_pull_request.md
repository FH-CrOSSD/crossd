# Change/Pull Request 
>(CHAOSS, 2023)

## Description

Change requests, or in terms of GitHub known as pull requests, are
proposals of code changes which can be accepted or declined and
respectively merged into the origin code or be discarded. States, a pull
request can be assigned to, are closed, opened and merged. This
information is required to gain insight into a project's development
process and the coding activities[^6].

## Parameters

$P_{i} = \ \{ i,\ i\ \text{is}\ \text{created}\ \text{pull}\ \text{request}\ \text{with}\ \text{all}\ \text{states}\ \}$

$C_{i} = \ \{ i,\ i\ \text{is}\ \text{created}\ \text{pull}\ \text{request}\ \text{with}\ \text{state}\ \text{closed}\}$

$O_{i} = \ \{ i,\ i\ \text{is}\ \text{created}\ \text{pull}\ \text{request}\ \text{with}\ \text{state}\ \text{open}\}$

$$M_{i} = \ \{ i,\ i\ \text{is}\ \text{created}\ \text{pull}\ \text{request}\ \text{with}\ \text{merged}\_\text{at}\ \text{date}\}$$

## Submetrics

+----------------------------------------------------------------------+
| ### a.  **Total pulls** (adopted)                                    |
+======================================================================+
| #### **Result**:                                                     |
|                                                                      |
| Total number of pull requests including all states.                  |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| Value represents a project's coding activity.                        |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $n(C)$                                                               |
+----------------------------------------------------------------------+
| ### b.  **Average pull closing time** (created)                      |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Average number of days required to close a pull request.             |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A short time span between the creation and closing of a pull request |
| indicates a high development velocity.                               |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $A_{d} = \{ d,d = Diff                                               |
| erence\ of\ creation\ and\ closing\ of\ a\ pull\ request\ in\ days\}$|
|                                                                      |
| $average\_ pull\_ closing\_ days = \left\lbrack \left                |
| ( \sum_{}^{}A_{d} \right)\text{/}n\left( C \right) \right\rbrack$ *  |
|                                                                      |
| *$\text{Let\ }                                                       |
| \left\lbrack x \right\rbrack\text{\ mean\ the\ integer\ closest\ to\ |
| x}$                                                                  |
+----------------------------------------------------------------------+
| ### c.  **Open to total pull requests ratio** (created)              |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Returns the ratio of open pull requests to the total number of pull  |
| requests as a value between 0 and 100.                               |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A high percentage of open requests implicates a high level of        |
| interest into a project's progress as well as there may be more      |
| requests than the reviewers are able to review which can result in a |
| development stall.\                                                  |
| Since this metric may result in a positive or negative conclusion,   |
| an additional analysis with other metrics may provide a higher       |
| information value.                                                   |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$ratio\_ open\_ total = \ (n(O)/n(P)) \times 100$$                  |
+----------------------------------------------------------------------+
| ### d.  **Closed to total pull requests ratio** (created)            |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Returns the ratio of closed pull requests to the total number of     |
| pull requests as a value between 0 and 100.                          |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| An active request review activity results in a high closed pull      |
| ratio, indicating a regular maintenance process.                     |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$ratio\_ closed\_ total = \ (n(C)/n(P)) \times 100$$                |
+----------------------------------------------------------------------+
| ### e.  **Merged to total pull requests ratio** (created)            |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Returns the ratio of merged pull requests to the total number of     |
| pull requests as a value between 0 and 100.                          |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A high percentage of merged pull requests may result from an active  |
| contributing community and active reviewers, underlining the         |
| project's development velocity.                                      |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$ratio\_ merged\_ total = \ (n(M)/n(P)) \times 100$$                |
+----------------------------------------------------------------------+

## Limitations

The listed sub metrics aim to provide an insight into projects pull
requests, a historical comparison of the data could provide crucial
insights into a project's evolution including the raise or decrease of
requests and acceptations. Additionally, the data could be expanded with
contributors' data. Due to feasibility, such analysis is excluded from
this thesis.

## Adaptions
/

## Implementation

To ensure that all merged pull requests are detected correctly, the
"merged\_at" parameter is utilized instead of the state to avoid
omitting pull requests which have been merged but are assigned to the
"closed" state.

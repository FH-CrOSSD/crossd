# Technical Fork 
>(CHAOSS, 2023)

## Description

Forks represent copies of a project on the same platform, used to
implement changes separately before the new code is merged into the
original repository. The information about forks provides an insight
into a project's extent of contributions and public interest as well as
the development progress. For following metrics, the forks are only
included if they were created in a selected period of 6 months.\
(CHAOSS, 2023) includes the question about how many forks a project has
and mentions already provided implementations. Following sub metrics are
based on these suggestions[^3].

## Parameters

$$F_{i} = \ \{ i,\ i\ \text{is}\ \text{created}\ \text{fork}\}$$

$$C_{i} = \ \{ i,\ i\ \text{is}\ a\ \text{contributing}\ \text{fork}\}$$

$$N_{i} = \ \{ i,\ i\ \text{is}\ a\ \text{non} - \text{contributing}\ \text{fork}\}$$

## Submetrics

+----------------------------------------------------------------------+
| ### a.  **Total number of created forks** (adopted)                  |
+======================================================================+
| #### **Result:**                                                     |
|                                                                      |
| Count of the created forks.                                          |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A high number of created forks indicates a high level of interest    |
| and a high development velocity.                                     |
+----------------------------------------------------------------------+
| #### **Formula:**                                                    |
|                                                                      |
| total\_forks = $n(F)$                                                |
+----------------------------------------------------------------------+
| ### b.  **Average forks created per week** (created)                 |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Integer, representing how many forks were created in a week.         |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| The more forks are created per week, the higher may be the interest  |
| to contribute to a project and raise the development velocity.       |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $E_{w} = \{ w,w = elementsperweek\}$                                 |
|                                                                      |
| $average\_ forks\_ created\_ per\_ week = \left\lbrack \left         |
| ( \sum_{}^{}E_{w} \right)\text{/}n\left( F \right) \right\rbrack$*   |
|                                                                      |
| *$\text{Let\ }\left                                                  |
| \lbrack x \right\rbrack\text{\ mean\ the\ integer\ closest\ to\ x}$  |
+----------------------------------------------------------------------+

## Limitations

In this thesis the fork metrics are calculated for a predefined time
period. For historical insights, more data is required. No information
about whether a fork has contributed or not is included in this work.
Not all forks merge the changes back, these are considered
non-contributing forks, those which attempt to merge are considered as
contributing forks. The retrieval of this information requires more data
as for instance the pull requests. Since forks represent a tree
structure, the collection progress is unpredictably complex and thus
determined as not feasible for this thesis.

## Adaptions

To maintain feasibility, forks are only included if they were updated in
the last 6 months.

## Implementation

The GitHub API offers no parameter to filter forks by their date, thus
forks are sorted by the "newest" parameter. The pages are queried until
an element is found with an "updated\_at" value, older than one year to
reduce the number of requests. Afterwards the elements are filtered
again, to return only data of the selected time period. It is unclear to
which information the "sort" parameter refers to, thus it cannot be
excluded that data is missing. For instance, if it concerns the
"created\_at" date, elements which were created more than 6 months ago
but have been updated during this period could be missing.

# Churn
>(Munson & Elbaum, 1998) (Alexan, Garem, & Othman, 2016)

## Description

The Churn implemented in (Alexan, Garem, & Othman, 2016) calculates the
metric in a weighted manner by considering bug fixing code changes, this
is not feasible for this thesis since bugs must be defined and detected
first. Yet, the churn is the only metric which provides an insight into
the code development itself, thus a simpler formula, adapted to the
available information is utilized. As the churn aims to represents
latest coding activities, data from the last month is included.

## Result

Represents the code change rate in percentage, a rate over 100% means
more lines have been deleted than added, a lower rate indicates more
lines have been added.

## Interpretation

An exceptional low rate implies new code has been added and may be
adapted in the future, an exceptional high rate on the other hand
indicates the code has been cleaned, thus during occasional code
development, the rate should be rather in the middle.

## Limitations

Since usual code metrics are calculated by the file content itself,
customized methods required for each programming language would be
necessary. This approach would require the processing of each file for
each project and goes beyond the scope of this thesis.

## Formula

$$\text{churn}\  = \ \frac{\#\ \text{of}\text{\ \ }\text{deleted}\ \text{lines}}{\#\ \text{of}\ \text{written}\ \text{lines}} \times 100$$

## Parameters: 

/

## Adaptions

The churn is calculated by the number of code lines which have been
added or deleted.

## Implementation

The GitHub API returns for each commit the added and deleted lines, as
mentioned all commits from the last month are included. If at least
1.000 commits have been contributed in this time periods, only the top
999 commits are included.

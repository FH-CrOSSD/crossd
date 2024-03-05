# Number of Support Contributors 
>(Madaehoh & Senivongse, 2022) (Foucault, Teyton, Lo, Blanc, & Falleri, 2015) (Zhong, Yang, & Keung, 2012) (Wang & Wu, 2022)

## Description

The formula to this metric is presented by (Madaehoh & Senivongse, 2022)
and based on a BRR report from 2005 (BRR 2005 - RFC, 2005). The number
of contributors is subdivided in score groups from 1 to 5, the scores
are used to calculate the final score.

## Result

The score represents a value in the range of 20 and 100.

## Interpretation

A high number represents a large community of support contributors, a
low number a small community.

## Limitations

The score groups are adopted, hence the representativeness is dependent
on the appropriation of the value ranges per group.

## Parameters

$$\mathbf{S}\  = \ \#\ \mathbf{\text{of}}\ \mathbf{\text{Contributors}}\ \mathbf{\text{and}}\ \mathbf{\text{Core}}\ \mathbf{\text{Team}}\ \mathbf{\text{Members}}$$

$\mathbf{S}\  = \ \mathbf{1}$ \< 5 persons

$\mathbf{S}\  = \ \mathbf{2}$ 5-10 persons

$\mathbf{S}\  = \ \mathbf{3}$ \> 10-20 persons

$\mathbf{S}\  = \ \mathbf{4}$ \> 20-50 persons

$\mathbf{S}\  = \ \mathbf{5}$ \> 50 persons

## Formula

$$V_{4} = \ \frac{S}{5} \times 100$$

## Adaptions

In the original report data from the past 6 months is included. Thus,
the formula is extended by a corresponding filter to reduce computing
costs.

## Implementation

As support contributors are considered users with commits to a
repository, commits are included from the past 6 months.

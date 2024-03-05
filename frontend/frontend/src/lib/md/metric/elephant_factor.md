# Elephant Factor 
>(CHAOSS, 2023)

## Description

This metric expresses the distribution of contributions by the community
across the companies the contributors belong to.

## Result

Total number with the value 1 or higher, for instance an elephant factor
of 2 means that more than 50% of the contributions are committed by 2
companies.

## Interpretation

According to the provided definition[^14], a project with a low elephant
factor may be more vulnerable to decisions by a small number of
companies. The volume of contributions should be considered in the
interpretation for a more reliable conclusion.

## Limitations

The elephant factor is not supposed to be a main source when considering
selecting an OSS, it is recommended to use it complementary to user
metrics and information.

## Formula

$$\text{elephant}\_\text{factor}\  = \ \text{Number}\ \text{of}\ \text{elements}\ \text{required}\ \text{to}\ \text{calculate}\ T_{2}$$

$$T_{1} = \sum_{\max(i)}^{min(i)}i \times 0.5$$

$T_{2} = \text{Highest}\ \text{contributions}\ \text{summed}\ \text{up}\ \text{until}\ \text{sum}\  > \ T_{1}$

$i$ = \# of Contributions per Organization

## Parameters
/

## Adaptions

The metric includes the commits of the previous 6 months, to retrieve a
representation of the current state of the project. Additionally, only
the top 20% of the most active contributors are included.

## Implementation

For retrieving the organization involved in a project, the contributors
are gathered first, and afterwards for each contributor the associated
organizations are retrieved. Since the number of contributors is
exceptionally high for popular projects, only the top 20% of
contributors with the most contributions are included. This method is
based on the pareto principle, otherwise, the number of API calls would
not be feasible.

# Code Dependencies
>(Upstream Code Dependencies (CHAOSS, 2023))

## Description

Code Dependencies are a crucial information about the criticality of a
project as they reflect the dependencies and connections to other
projects.

This metric includes two sub-metrics, dependency upstream dependencies
which concern a project's dependency on other projects and downstream
dependencies, which concern those repositories which depend on a
project.

## Parameters

$$P_{i} = \{ i,\ i = \ \text{GitHub}\ \text{project}\}$$

$U_{d}\  = \ \{ d,\ d\  = \ \text{projects}\ \text{depending}\ \text{on}\ P_{i}\ \}$

$D_{d}\  = \ \{ d,\ d\  = \ \text{projects}\ P_{i}\ \text{depends}\ \text{on}\}$

$$V_{d}\  = \ \{ d,\ d\  = \ \text{public}\ \text{projects}\ P_{i}\ \text{depends}\ \text{on}\}$$

## Submetrics

+----------------------------------------------------------------------+
| ### a.  **Upstream dependencies** (adapted)                          |
+======================================================================+
| #### **Result**:                                                     |
|                                                                      |
| Total number of unique upstream dependent projects, represented by   |
| software packages included in the project. Packages are code         |
| containers which include for instance a certain project version.     |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A high number of dependencies may pose a risk since a failing        |
| software the project depends on can have negative effect on the      |
| concerned project.                                                   |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $total\_ upstream\  = \ n(U)$                                        |
+----------------------------------------------------------------------+
| ### b.  **Downstream dependencies (created)**                        |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Total number of downstream dependent projects, represented by other  |
| GitHub projects, including public and invisible projects.            |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A high number of dependents implies the projects criticality and     |
| relevance for other projects.                                        |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $total\_ downstream = \ n(D)$                                        |
+----------------------------------------------------------------------+

## Limitations

The proposed upstream metric includes direct and indirect dependencies,
yet these are limited to the functionalities of GitHub, referring to
repositories lock files and the supported ecosystems[^12]. Another
approach to retrieve indirect dependencies is to gather the dependencies
of dependent projects recursively. Due to the large number of
dependencies per project and the unpredictable amount of time and
calculation cost, this is out of scope from this thesis.

## Adaptions

The metrics include upstream and downstream dependencies.

## Implementation

Retrieving dependencies from GitHub projects is limited to either
checking dependency differences from single commits, check the file
contents or reading the dependency graph. The dependency graph is the
most reliable data source, yet there is no API endpoint to this
information, thus a web scraper is implemented to gather dependencies,
upstream as well as downstream. Dependencies occurring multiple times in
different files are only included once.

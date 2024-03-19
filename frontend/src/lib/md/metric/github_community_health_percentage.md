# Github community health percentage [^8]

## Description

This percentage score represents the existence of several files such as
the readme or the contributing file. Since the formula published by
GitHub is outdated as of 22.07.2023 by considering incomprehensible
scores, a custom formula is defined additionally to cover this
information in a transparent way.

## Parameters

$F_{d}\  = \ \{\text{readme},\ \text{contributing},\ \text{license},\ \ \text{code}\_\text{of}\_\text{conduct},\ \text{description},\\
\ \text{issue}\_\text{template},\ \ \text{pull}\_\text{request}\_\text{template},\ \text{documentation}\}$

$$F_{d}\  = \ \{ d,\ d\ \text{is}\ \text{documentation}\ \text{information}\}$$

$F_{e}\  = \ \{ e,\ e\ \text{is}\ \text{available}\ documentation\ information\}$

$F_{n}\  = \ \{ n,\ n\ \text{is}\ \text{not}\ \text{available}\ documentation\ information\}$

## Submetrics

+----------------------------------------------------------------------+
| ### a.  **GitHub community health percentage score** (adopted)       |
+======================================================================+
| #### **Result**:                                                     |
|                                                                      |
| A value between 0 and 100, representing the extent of existing       |
| documentation files.                                                 |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A high value represents a well-maintained documentation state of a   |
| project.                                                             |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $\ $As mentioned in the description, the formula proposed by GitHub  |
| is outdated.                                                         |
+----------------------------------------------------------------------+
| ### b.  **Custom GitHub community health percentage score** (adapted)|
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| A value between 0 and 100, representing the extent of existing       |
| documentation files.                                                 |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| A high value represents a well-maintained documentation state of a   |
| project, with a higher information value than the adopted metric due |
| to including all available documentation information. Can be         |
| compared to the origin health score for a validity check.            |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $cust                                                                |
| om\_ health\_ score\  = \ (n(F)\ /\ \sum_{}^{}{F_{d}) \times 100}\ $ |
+----------------------------------------------------------------------+
| ### c.  **Existence of single documents and information** (created)  |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Boolean value for each file, 1 represents the existence, 0 the       |
| non-existence.                                                       |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| The existence of single files has low information value for single   |
| repositories, more insights can be provided by a comparison over all |
| repositories. According to the overall existence, files may be       |
| assigned to a weight for further analysis in the future, which are   |
| out of scope from this thesis.                                       |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$f\left( x \right) = \left\{\begin{matrix}                          |
| 1,\ \ \& x \in \ F_{d}\\                                             |
| \ 0,\ \ otherwise \\                                                 |
| \end{matrix} \right.\ $$                                             |
+----------------------------------------------------------------------+
| ### d.  **Total number of existing files** (created)                 |
+----------------------------------------------------------------------+
| #### **Result**<span class="underline">:</span>                      |
|                                                                      |
| Number of existing information for the corresponding files, returns  |
| a value in the range of 0 and 8.                                     |
+----------------------------------------------------------------------+
| #### **Interpretation**<span class="underline">:</span>              |
|                                                                      |
| A high number represents a maintained project's documentation and    |
| gives the impression of a high-quality level project.                |
+----------------------------------------------------------------------+
| #### **Formula:**                                                    |
|                                                                      |
| $true\_ count\  = \ n(F_{e})\ $                                      |
+----------------------------------------------------------------------+
| ### e.  **Total number of non-existing files** (created)             |
+----------------------------------------------------------------------+
| #### **Result**<span class="underline">:</span>                      |
|                                                                      |
| Number of not existing information for the corresponding files,      |
| returns a value in the range of 0 and 8.                             |
+----------------------------------------------------------------------+
| #### **Interpretation:**                                             |
|                                                                      |
| A high number represents an unmaintained project's documentation and |
| gives the impression of a low-quality level project.                 |
+----------------------------------------------------------------------+
| #### **Formula:**                                                    |
|                                                                      |
| $$false\_ count\  = \ n(F_{n})$$                                     |
+----------------------------------------------------------------------+

## Limitations

The proposed metrics are dependent on the available information provided
by GitHub. Thus, other information such as project requirements are not
included.

## Adaptions

The adapted health score includes all available information about
provided files and documentations.

## Implementation

For each information the existence of data is checked, and a
representative Boolean value is assigned.

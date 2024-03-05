# Contributions Distributions 
>(Bus Factor (CHAOSS, 2023) (Goggins, Lumbard, & Germonprez, 2021) & Pareto Principle (Goggins, Lumbard, & Germonprez, 2021) (Aman, Burhandenny, Amasaki, Yokogawa, & Kawahara, 2017))

## Description

Knowledge about the distribution of contributions across different
contributors is required to ensure that a project has a stable number of
core maintainers. To less maintainers propose a risk of the project to
stall, to many maintainers may lead to a project where no one is in
charge. Signs for these risks can be detected by metrics such as the bus
factor and by reviewing the pareto principle. As contributions are
considered commits for following metrics. The principle behind the
pareto is defined as following:

Total Number of collaborations by top 20% of contributors with the most
collaborations should be 80% of the total contributions.\
The pareto principle is reviewed for two attributes, the Number of
Commits (NoC) and the Ratio of Files (RoF), as proposed in (Aman,
Burhandenny, Amasaki, Yokogawa, & Kawahara, 2017). As (Aman,
Burhandenny, Amasaki, Yokogawa, & Kawahara, 2017) refers to the
contributors with the most contributions to the dominant, and to the
others the tail part, these terms are used respectively. Additionally,
as proposed in (Alexan, Garem, & Othman, 2016), the average number of
contributors per file are included. As total files are all files
considered which received a commit.\
As in following metric concerning the number of contributors, for this
metric the contributions data is included for the past 6 months.

## Parameters

$C_{i} = \{ i,i = Number\ of\ commits\ per\ contributor\}$\*

\* *Values ordered descending*

$F_{i} = \{ i,i = \ Number\ of\ contributors\ per\ each\ file\}$\*

## Submetrics

+----------------------------------------------------------------------+
| ### a.  **Bus Factor** (adopted)                                     |
+======================================================================+
| #### **Result**:                                                     |
|                                                                      |
| A total number equal or larger than 1.                               |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| Represents the risk factor if the most active contributors stop      |
| contributing by calculating the smallest number of people            |
| contributing 50 % of the contributions. This means if one            |
| contributor commits over 50 % of the contributions, the bus factor   |
| score would be 1. Thus, a low number proposes a risk of the project  |
| to stall if the most active contributor stops contributing.          |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| > $\text{Bus\ Factor\ }                                              |
|        Score\  = \ \#\ of\ Elements\ required\ to\ calculate\ T_{2}$ |
|                                                                      |
| $$T_{1} = \sum_{max(i)}^{min(i)}C_{i} \times 0.5$$                   |
|                                                                      |
| $i$ = \# of Contributions per Contributor                            |
|                                                                      |
| $T_{2} = Highest\ contributions\ summed\ up\ until\ sum\  > \ T_{1}$ |
+----------------------------------------------------------------------+
| ### b.  **Pareto Principle (RoF & NoC)** (adopted)                   |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Return includes the percentage of contributors who contributed 80%   |
| of the commits or file changes. The ratio of the commits is          |
| calculated by the number of commits, and the ratio of the files by   |
| the number of edited files per contributor. The actual number of     |
| contributions for the top contributors is calculated, and finally    |
| the difference between the aimed and the number of contributors is   |
| calculated in percent. The difference is represented as a percentage |
| between 0 and 100.                                                   |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| The returned percentage should be as low as possible, indicating     |
| that the distribution of the contributions aligns with the pareto    |
| principle.                                                           |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $$O_{i} = \{ i,i = RoF\ or\ NoC\ per\ contributor\}$$                |
|                                                                      |
| $$dominant\_ contributions\  = \ n(C_{i}) \times 0.8$$               |
|                                                                      |
| $$percentage\ of\ contributors\ with\ 80\%\ of\ c                    |
| ontributions = \sum_{i\  = dominant\_ contributions}^{min(i)}O_{i}$$ |
|                                                                      |
| $i$ = index number of contributor                                    |
|                                                                      |
| $$diff\_ pareto\  = \ |0.20\  - \ (pareto)|\  \times 100$$           |
+----------------------------------------------------------------------+
| ### c.  **Average contributors per file** (adapted)                  |
+----------------------------------------------------------------------+
| #### **Result**:                                                     |
|                                                                      |
| Average number of contributors per file with a value equal or higher |
| than 1.                                                              |
+----------------------------------------------------------------------+
| #### **Interpretation**:                                             |
|                                                                      |
| The result is a simple score, which gets a higher information value  |
| when compared with other repositories or correlated with similar     |
| metrics. A value close to 1 represents the risk, mentioned in the    |
| interpretation of the bus factor.                                    |
+----------------------------------------------------------------------+
| #### **Formula**:                                                    |
|                                                                      |
| $avg\_ num\_ contriutors\_ per\_ file = (\sum_{}^{}F_{i})/n(F)$      |
+----------------------------------------------------------------------+

## Limitations

The pareto principal analysis is limited to the 80%, for a more detailed
view this could be expanded to each quantile or in detail as visualized
in (Aman, Burhandenny, Amasaki, Yokogawa, & Kawahara, 2017). Further,
the total number of files includes only those files, which received a
commit in the selected time period. For the total number of all files of
a repository, it would be necessary to query the entire content, which
is out of scope in terms of calculation and time costs.

## Adaptions

The number of contributors is calculated as average to return one value
for each repository.

## Implementation

The calculation of the above metrics includes all commits and queries
each single commit from the past 6 months to retrieve the concerned
files and possible co-authors for each commit. Due to the high
performance costs of querying single commits, the query is stopped at
1.000 commits, resulting in a maximum of 999 commits.

The contributors are distinguished by their e-mail address, as users can
have several user names. If a user is verified by GitHub, the author's
e-mail address is taken. For instance, changes committed directly on the
GitHub page have the default committer "GitHub" assigned, the user who
submitted the change is in the author field respectively. Depending on
the location from where the change is committed, the e-mail address can
vary too, thus in individual cases it is possible that single users are
counted as different contributors.

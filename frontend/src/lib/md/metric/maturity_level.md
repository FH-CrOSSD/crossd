# Maturity Level 
>(Madaehoh & Senivongse, 2022)

## Description

Considered as quality metric, this measure includes a repositories age,
issues and releases. The issues and minor releases are counted and all
values, including the age, are subdivided in group. Each group is
represented by a score in the range of 0-5. For this metric, a low
number of issues and a high number of minor releases and a higher age
are considered positive.

## Result

The returned score is a value in the range of 20 -- 100, whereas a
higher score indicates a better quality then a lower score.

## Interpretation

The returned level score represents the maturity. Regarding the
parameters in this metric, the maturity refers to the development stage.
For instance, a project in a late development stage with fewer issues,
more releases and a higher age would result in a higher score than a
project in an earlier stage.

## Limitations

The parameters are subdivided in groups by absolute value ranges. Thus,
the information value of the maturity level depends on other factors
such as the popularity and development speed of a project, respectively
influencing the number of issues and number of releases.

## Formula

$$((M\_ 1 + M\_ 2 + M\_ 3)/3) \times \ 100$$

## Parameters

$$M_{1} = \ \frac{S_{\text{age}}}{5}$$

$S_{\text{age\ }} = 1$ Age \< 2 months

$S_{\text{age}} = 2$ Age 2-12 months

$S_{\text{age}} = 3$ Age \> 1- 2 years

$S_{\text{age}} = 4$ Age \> 2-3 years

$S_{\text{age}} = 5$ Age \> 3 years

$$M_{2} = \ \frac{S_{\text{issue}}}{5}$$

$S_{\text{issue}} = 1$ Nr. of issues\* \> 1000

$S_{\text{issue}} = 2$ Nr. of issues\* \> 500-1000

$S_{\text{issue}} = 3$ Nr. of issues\* \> 100-500

$S_{\text{issue}} = 4$ Nr. of issues\* \> 50-100

$S_{\text{issue}} = 5$ Nr. of issues\* $\leq$ 50

\*in the past 6 months

$$M_{3} = \ \frac{S_{\text{release}}}{5}$$

$S_{\text{release}} = 1$ Nr. of releases\* 0 version

$S_{\text{release}} = 3$ Nr. of releases\* 1-3 versions

$S_{\text{release}} = 5$ Nr. of releases\* \> version

\*in the past 12 months

## Adaptions

Instead of only minor releases, all releases are included since no
method to differentiation is presented.

## Implementation

Issues and Releases are filtered as mentioned in the formula by the
GitHub APIs "since" parameter, referring to the time the object was last
updated. Since no definition of minor releases is provided, all releases
are included in the implementation.

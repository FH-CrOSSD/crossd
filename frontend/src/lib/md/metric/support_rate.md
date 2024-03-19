# Support Rate 
>(Madaehoh & Senivongse, 2022)

## Description

The support rate refers to issues and pulls which received a response
during the last 90 days. As responses are considered comments. This
metric provides an insight into the support availability over a
project's community. The formulas are implemented as recommended and
documented below.

## Result

The returned value is in the range of 0 to 100, a high value mirrors a
high support rate.

## Interpretation

A high support rate implies a high communication activity across the
community and developers. Thus, this metric provides crucial insights
into the support routine of developers and users.

## Limitations

This metric does not consider how many responses were received and
assumes the first response to be supporting, which may not be always the
case. Another factor which is not included in this metric is the time
until an issue is finally resolved. If an issue cannot be resolved by a
single answer, the support process includes more effort than a single
response.

## Parameters

$M_{1}$ Issue Support Rate

$M_{2}$ Pull Request Support Rate

$$M_{1} = \begin{Bmatrix}
\left( \frac{\begin{matrix}
\text{Number\ of\ issues\ } \\
\text{that\ have\ been\ responded\ } \\
in\ the\ past\ 90\ days \\
\end{matrix}}{N} \right),N > 0\ \  \\
0,\ N = 0\ \ \  \\
\end{Bmatrix}$$

$$where\ N\ Total\ issues\ in\ the\ past\ 90\ days$$

$${M_{2} = \begin{Bmatrix}
\left( \frac{\begin{matrix}
\text{Number\ of\ pull\ requests\ } \\
\text{that\ have\ been\ responded\ } \\
in\ the\ past\ 90\ days \\
\end{matrix}}{N} \right),N > 0\  \\
0,\ N = 0\ \ \  \\
\end{Bmatrix}
}{where\ N\ Total\ pull\ requests\ in\ the\ past\ 90\ days}$$

## Formula

$$V_{5} = \ \left( \frac{M_{1} + \ M_{2}}{2} \right) \times 100$$

## Adaptions

Originally, the data of a time period of 6 months is included. Due to
the calculation costs, the time was reduced to 90 days.

## Implementation

Issues and pull requests are gathered via the GitHub APIs issue
endpoint, the comments are retrieved by the corresponding comments
endpoint for each issue/pull request separately.

# OSI Approved Licenses 
>(CHAOSS, 2023)

## Description

OSI approved license ensure the open-source state of a project as the
Open Source Initiative (OSI) conducts a license review process to
confirm the compliance with the open source definition[^1]. Since this
thesis concerns OSS, this information is indispensable.

## Result

The return of this metric is Boolean, if the license of a project is OSI
approved the value is 1, if it is not approved or no license is
available the result is 0.

## Interpretation

Additionally, to the confirmation of the OS status, the availability of
this information represents how well documented a project is.

## Limitations

The existence of one file may not be sufficient to provide a
confirmation of the OSS state of a project. Further, it is possible that
licenses are not retrievable by the API as they are individually defined
for the corresponding project. In this case GitHub assigns the project
the spdx id "NOASSERTION".

## Parameters

$$P_{l}\  = \ \{ l,\ l\ is\ a\ spdx\ license\ id\}$$

$$O_{l} = \ \{ l,\ l\ is\ an\ OSI\ approved\ spdx\ license\ id$$

## Formula

$$Ifx\ is\ not\ None:$$

$$f\left( x \right) = \left\{ \begin{matrix}
osi\_ approved,\ \ \& x \in \ O_{l} \\
not\_ osi\_ approved,\ \ \& x\  \in \ N \\
not\_ found,\ \ \ \ \ \ \ \ \ \& x \notin \ P_{1}\  \\
\end{matrix} \right.\ $$

$$Else:\ f(x)\  = not\_ provided$$

## Adaptions

(CHAOSS, 2023) recommends calculating how many licenses of a project are
OSI approved or calculating the percentage of approved files of a
project. Checking all files of each project is out of scope for this
thesis, thus the existence of a license for each repository is
considered as sufficient.

## Implementation

If a license is provided, the OSI status is verified by the spdx license
list available on GitHub[^2].

$$N_{l} = \ \{ l,\ l\ \text{is}\ a\ \text{not}\ \text{OSI}\ \text{approved}\ \text{spdx}\ \text{license}\ \text{id}$$

$P_{l} \supset \ \{ O_{l}$, $N_{l}$}

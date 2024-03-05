# Size of Community 
>(Madaehoh & Senivongse, 2022)

## Description

This metric resembles the support contributor metric, additionally
including watchers.

## Result

The score represents a value in the range of 20 and 100.

## Interpretation

A large community including watchers and a high score represents a
project's popularity and relevance across other projects.

## Limitations

The scores are assigned to the recommended value ranges, for more
fitting groupings, an analysis of the selected data would be necessary
preliminarily.

## Parameters

$$S = \text{Number}\ \text{of}\ \text{Core}\ \text{Team}\ Members,\ Contributors\ and\ Watchers$$

$S\  = \ 1$ Small (\<50 people)

$S\  = \ 2$ Relatively Small (50-100 people)

$S\  = \ 3$ Medium (\> 100-200 people)

$S\  = \ 4$ Relatively Large (\> 200-300 people)

$S\  = \ 5$ Large (Total \> 300 people)

## Formula

$$V_{2} = \ \frac{S}{5} \times 100$$

## Adaptions 
/

## Implementation

In GitHub terms watchers correspond to a project's stars and subscribers
represent user who watch a project to follow the progress[^15]. Thus, as
number of watchers the subscribers\_count value is gathered. Core team
members are to be considered as part of the contributors

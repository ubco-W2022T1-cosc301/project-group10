# Group 10 - Analyzing NHL Predictions

![Ice Hockey](images/ice_hockey1.jpg)

## Introduction

### Description of our topic

Our topic at its broadest is simply "hockey," but that's not a very helpful description. More specifically, we're interested in analyzing a few trends in National Hockey League games that we feel may (or demonstrably *do*) have an effect on the outcomes of games -- home ice advantage, travel time, and the effect of intra-divisional matchups on the total score of a game. Sports as a source of data isn't entirely new; baseball is perhaps most famous for fans' obsessive tracking and analysis of game data. But hockey is equally valuable for data analysis, and at any rate it interests our group much more than baseball. In our analytics project, we hope to show whether travel time had any significant impact on teams' records last season, as well as potentially reconfirming the value of a "home advantage." Seeing the potential effect of divisional matchups on games is an interesting topic to us as well, as the four-point swing in a playoff race is often said to incentivize teams to push harder and possibly score higher. A dashboard could absolutely be built for this -- while some (e.g. home ice advantage) may not be especially interesting to look at in a dashboard, visualizations for the "net change in win rate, by distance from home city" could drive a lot of interest.

### Description of dataset

This data set was provided by FiveThirtyEight and is a forecast of the 2021-2022 NHL season. While they have a data set with every game since the inaugural season in 1917-1918, we chose last year’s data as it would have both predicted and actual outcomes of games. The data set gives each team a rating and tries to predict the outcome of the rest of the season based on thousands of simulated games. Throughout the season with each actual game played, the ratings of each team are updated and the simulation process is repeated. It is hard to know FiveThirtyEight’s purpose for the data set beyond an initial article, but they have prediction models for almost every sport that are all very reputable. The data set only requires the scores of each game and if they went into overtime/shootout to calculate the ratings. A little fun fact, NHL data is collected by a team of “scorers” at each stadium who keep track of every possible game time stat.

Supplementary data for the distance between NHL cities has been provided by deep13.xyz. The data set, very simply, is a 32-by-32 table containing the distances between each NHL city and each of the others, in kilometers. The distance is "as the crow flies," based on the geographic coordinates of each NHL arena. The source itself states that the coordinates are "according to the internet, which is never wrong," which raises some slight concerns about the authenticity of the data; however, randomly chosen pairs of cities have accurate distances according to a Google Maps check.

Supplementary data for the average NHL attendance has been provided by statista.com with the original data coming from ESPN.com in July of 2022. The data shows average attendance of every NHL team for the 2021-2022 season.


## Exploratory Data Analysis

We conducted an EDA by creating the correlation plot comparing the columns against eachother. This helped us identify all of the columns in the dataset, as well as helping us identify if there were any interesting correlations between them!

![Correlation Plot](images/EDA_corrPlot.png)

There are a few interesting trends that appear in the correlation map. The obvious ones are that home and away ratings are positively correlated with the corresponding win probabilities, also that ratings are loosely correlated to the points they will score. The interesting one I found was that the overtime probability was posititely correlated with the away team's win probability! Game importance which is a score on how much the result will affect playoff odds is interesting since it doesnt seem to be correlated to any other column, so 538 must have more data that they aren't sharing!


To visualize the correlation between overtime probability and team's win probability, I decided to graph them on a scatterplot

![overtime_prob Plot](images/EDA_overtime_prob.png)

While the overtime probability is directly correlated to the ratings, it's interesting to see that the highest probability of overtime occurs when the home team has a ~50 point disadvantage to the away team! I assume this is because being the home team gives an advantage, so this helps us see that the advantage is around 50 points. 


Following the previous scatterplot, I wanted to see if my conclusion that teams with a -50 rating differential had the most overtimes. To check, I plotted the amount of times teams went into either overtime or a shootout in the regular season. 

![overtime_count Plot](images/EDA_overtime_games.png)

Chicago, Detroit, Minnesota and Tampa were leading the count! The first two make sense as they were average to below average teams during the 2021 season, but Minnesota and Tampa were both top 3 in their division. Very interesting

One last thing I wanted to see was how the rating difference changed throughout the season. I visualized this using a lineplot.

![rating_diff Plot](images/EDA_ratingdiff.png)


This graph is interesting to delve into, since the 538 algorithm works by setting most of the teams around the same rating at the start of the year with a little deviation in ratings based on the previous year. As the year goes on, teams start to deviate from the mean as good teams keep gaining points from winning and bad teams continually lose points from losing games. An interesting question that is brought up in this graph that is covered in Andrei's notebook is "when in the season can we have confidence in the predictions?"
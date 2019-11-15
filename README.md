# The Statistical Impact of Different Factors on Runs Scored in MLB Games

## The data
Major League baseball provides scores of historical information that are available to the public through their API. For the purpose of this project, we collected box score data, ballpark information, and weather data for all regular season MLB games for the 2009-2019 seasons.
## The goal
The aim of this project is to use the data collected from Major League Baseball to determine the statistical impact that the designated hitter, temperature, and ballpark have on total runs scored in a baseball game.

## Statistical Methods 

##### First Test 
To determine whether the designated hitter has a meaningful impact on runs scored, we grouped our games into two categories: one for the games played under National League rules (without a designated hitter) and another for games played under American League rules (with a designated hitter). We ran a two-sample Z test on the NL and AL games to determine if the designated hitter meaningfully impacts run production. The AL sample mean was 0.4 runs higher than the NL. Due to the large number of games used in the test, we can conclude that the difference in means between the two leagues is statistically significant (Z-Statistic = 7.3).

##### Second Test 
We used ordinary least squares regression to model the relationship between temperature and runs scored in a game. The correlation coefficient of our model is 0.08, with an R-squared of 0.007 and F-Stat of 196. This suggests that while the magnitude of the effect is relatively small, there is a consistent positive relationship between the temperature and total runs scored in a baseball game.

##### Third Test
Lastly, we used analysis of variance (ANOVA) to determine whether ballparks create a meaningful difference in run production. According to our findings, there is strong evidence to suggest that the arena baseball games are played in impact the amount of runs scored in a baseball game.


## Other Considerations and Further Exploration
While our test on different ballparks proves that there is a statistical difference between run production generally, between all stadiums, we would like to further explore which stadiums contribute most to the variance in run production between ballparks. Additionally incorporating these findings into a grander model that accounts for matchup specific information to predict the run total for a specific Major League baseball game is of particular interest.

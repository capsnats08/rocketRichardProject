README

This project aims to find the Rocket Richard winner who had the largest comeback to win their trophy. 

Caveat:
If Player A starts a game earlier than Player B on the same day, all of Player A's goals will count as happening before Player B, even if that is not what happened in real time. This is a limitation of the statistics that I was able to find from the NHL.com api, from the limited information I was able to find on it.

Results:

Pavel Bure missed some games early in the season, but finished incredibly strong, scoring 44 goals after January 8th, 1994 in order to capture the Rocket Richard trophy. He was at his lowest down 16 goals to Dave Andreychuk on January 8th, 1994. Andreychuck ended up finishing 4th in overall scoring, behind Bure, Brett Hull, and Fedorov.

Future capabilities: 

I'd like to provide a date where the largest deficit happens, if for no other reason than to make the verification of working code easier. 

Instead of passing tuples everywhere, I'd like to make classes for them. This was a quick hack, so I was not intending on it being a great display of engineering. 

Implement some better way to find out the number of games in a year instead of relying on NHL.com API to throw us a specific error. We shouldn't be relying on their error messaging staying the same. This would most likely just need to be a map, because special years with either strikes or lockouts would make simply taking the number of teams in the league and the number of planned games would make a data file necessary anyway (Another reason to hate lockouts... Thanks Bettman).

The biggest weakness of the data is that Pavel Bure was at his largest deficit on 01/08/1994, down either 16 goals to Dave Andreychuk. But because Bure plays on the west coast his game number is later. But this is not necessarily true, because Andrychuk could have scored late in his game and Bure could have scored early in his. But NHL.com does not provide timestamps of the goals, just the summary of the game. 



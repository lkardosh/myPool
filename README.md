# CIS 2750 Assignment 4
Website that allows users to play a game of 8-ball.
Includes: 
C library that implements a number of functions
to simulate the collision of billiard balls with cushions and other balls.
A database to create different tables filled with information about a game of Pool.
myServer.py, used to allow user to start a 2 player game of pool.



## Author Information

Name: Lauren Kardosh


Date: Mar 29 2024

## Using Code

### Dependencies

This program is built with C, Python, and html

### Building the program

To compile, write the command `make`, then "export LD_LIBRARY_PATH=`pwd`"


### Using the program

To run the server, enter `python3 myServer.py 'port number`


### Game Rules

-One player will play the lower numbered balls (1-7) while the other player will play the higher
numbered balls (9-15). Whoever sinks the first ball gets assigned that half of the balls. Once
the first ball has been sunk, the server should display “high” or “low” after the player’s name to
indicate which balls that player is playing.

-After sinking all their own balls, a player must sink the black (8) ball. Any player who sinks the 8
ball before sinking all their other balls automatically loses! Whoever sinks the 8 ball first (after sinking all their own balls) wins the game.

-If a player sinks and opponent’s ball, that ball is credited to their opponent, but there is no
other penalty.

-If a player sinks one of their own balls (even if they also sink an opponent’s ball, or the white
ball), they get another turn. Otherwise, the opponent gets a turn.



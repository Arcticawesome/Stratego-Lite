# Stratego-Lite

My version of Stratego in Python involves two battling sides on a 6 x 4 grid. Each side has a
flag they are defending, 3 bombs around its flanks, as long as the placement is in the first two
rows of their side, and 2 levels of infantry that can attack the opposing side. The first level of
infantry can defuse the stationary bombs and the second level of infantry can kill the first level.

The objective of this game is to capture the flag of the enemy.

Players: Human and AI command troops
Game mechanics: troop movement, combat resolution, and flag capture. Troops with higher values defeat weaker ones, and equal values result in mutual destruction.
System: Turn-based, allowing players to strategically move their units on a grid-based board. 
How does the AI work? Behavior for automatic troop movement and combat, using random choices for direction and prioritizing valid moves. 


This project decomposes the game into functions and then utilizes helper functions to create a one-player dynamic experience.

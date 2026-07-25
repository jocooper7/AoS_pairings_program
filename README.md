# AoS_pairings_program
Pairings program to analyze 5x5 differential matrices and determine ideal pairings for user decided opponent and map.

Author: Jo Cooper
Requirements: Pandas, Numpy

Set up: 
Program is run in a single .py in the CLI. 
I have provided a JSON that is currently filled with randomized differentials for testing.
Users can modify the JSON with their own differential values or modify faction_names. 

It is not recommended to modify the structure or key names.
Doing so has the potential to prohibit the program from running properly.

User team members, factions, and enemy teams can be modified inside the program under the Base Variables and Lists section.
Order of enemy_teams list does not matter, but spelling must match teams in JSON as enemy_teams list is used for validation

Extended Program Summary:
Program analyzes a differential matrix pulled from the JSON file. User determines the opponent team and current map. The program then pulls the data and creates a DataFrame.
Program then provides information to aid the user in determining mathematically optimal pairings based on projected differentials. 
Metrics include mean of differentials for each user army, standard deviation of these differentials, and an ideal pairings list based on maximum bipartite matching.
 - Each matrix is 5x5, allowing for brute forcing the math with only 5! (120) permutations.

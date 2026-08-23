# AoS_pairings_program
Pairings program to analyze 5x5 differential matrices and determine ideal pairings for user-decided opponent and map.

**Author:** Jo Cooper
**Requirements:** Python 3.x, Pandas, Numpy, JSONschema (`pip install pandas numpy jsonschema`)

## Setup
Run via `pairing_program.py` in the CLI:
------------------------------------------------------------------------------------------
A JSON file with randomized test differentials is included. Users can modify it with their own differential values or edit `faction_names`. User factions can also be changed during program use.

Enemy teams and maps are pulled from the JSON file. Teams can be in any order. Maps should be consistent in tense and spelling throughout. Including the same 5 maps for each team is required.

For opponent selection, users can either manually choose the enemy team or use the **random opponent mode**, which auto-selects an opponent for testing/quick play.

------------------------------------------------------------------------------------------
## Extended Program Summary
The program analyzes a differential matrix pulled from the JSON file. The user selects the opponent team and current map; the program pulls the relevant data and builds a DataFrame.

It then reports:
- Mean and median differentials for each user army
- Standard deviation of these differentials
- An ideal pairings list based on maximum bipartite matching

Each matrix is 5x5, so the pairing math is brute-forced with all 5! (120) permutations, implemented via `itertools`, to guarantee the true maximum-sum pairing rather than an approximation.

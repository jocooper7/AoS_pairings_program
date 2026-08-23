# imports
import itertools

import pandas as pd

# This file contains the brute force maximum path calculation function for the pairings program.

def maximum_path(df: pd.DataFrame, curr_total: int = 0) -> int:
    """
    Brute force maximum weight bipartite matching algorithm via permutation search.
    Solution does not scale well for larger matrices, but is acceptable for 5x5 and smaller square matrices.
    
    Parameters:
    df (pd.DataFrame): square matchup differential matrix as a pandas DataFrame.
    curr_total (int): The total differential from previous rounds, if applicable. Defaults to 0.

    Factions and enemy armies are pulled from the DataFrame's index and columns so the function may be reused for the later 3x3 matchup matrix.

    Returns:
    best_total (int): The maximum total differential achieved by the best pairings.
    """

    best_total = float('-inf')
    best_pairs = []


    factions = df.index.tolist()
    enemy_armies = df.columns.tolist()
    n = len(factions)
    diff_matrix = df.values

    # iterates through all permutations of enemy army matchups to find the maximum total differential for the given matchup matrix.
    for perm in itertools.permutations(range(n)):
        total = sum(diff_matrix[i][perm[i]] for i in range(n))

        if total > best_total:
            best_total = total
            best_perm = perm

    best_pairs = []
    for row, col in enumerate(best_perm):
        row_name = factions[row]
        col_name = enemy_armies[col]
        value = diff_matrix[row][col]
        best_pairs.append((row_name, col_name, value))

    print("\nBest Pairings:")
    for row_name, col_name, value in best_pairs:
        print(f"{row_name} vs {col_name} \n- Estimated Differential: {value}")
    final_total = best_total + curr_total
    print(f"\nMaximum Total Differential: {final_total} (including previous rounds' differentials if applicable)")

    return final_total
        
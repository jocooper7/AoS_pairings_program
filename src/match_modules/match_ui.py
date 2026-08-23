# imports
import random

import pandas as pd

from match_modules import match_validation as mv
from match_modules import maximum_path as mp

# This file contains the user interface functions for the pairings program.
# It handles the display of information, user prompts, and the flow of the program's logic during individual matchup steps.

def starting_display() -> None:

    print("\nWelcome to the AoS Teams Matchup Program.")
    print("This program will aid in the analysis of ideal matchups for a 5v5 Tournament.")

    print("\nWould you like an explanation of the pairings minigame?")
    print("If yes, an explanation will be provided. If no, the program will continue to the matchup selection.")
    start = False
    while not start: 
        explain = mv.boolean_validation("Enter yes/y or no/n: ")

        if explain:
            explanation_display()
        start = True

def display_team_selection(enemy_list) -> None:
    print("\nEnemy team options: ")
    for i, team in enumerate(enemy_list):
        print(f"{i + 1}. {team}")

def display_map_selection(maps_list) -> None:
    print("\nMap options: ")
    for i, map_option in enumerate(maps_list):
        print(f"{i + 1}. {map_option}")

def explanation_display() -> None:
    print("\nWhile Age of Sigmar is typically a 1v1 game, there are special 5v5 tournaments.")
    print("Overall score is determined by the differential of scores across all matchups.")
    print("-" * 100)
    print("To determine which team members play each other, a minigame is used to pair players.")
    print("This program simulates the minigame and provides insights into ideal match ups based on multiple metrics.")
    print("Metrics Include:\n- mean pairings differential\n- median pairings differential \
          \n- pairings standard deviation\n- ideal pairings from a brute force maximum bipartite matching algorithm.")
    print("-" * 100)
    print("Step 1: Each team selects an army to present to the opposing team. Once chosen, both teams reveal their selection.")
    print("Step 2: Teams select 2 armies as potential matchups for the presented army, and then the armies are revealed.")
    print("Step 3: Teams select which of the 2 opposing armies will go against their presented army.")
    print("This process is repeated with the remaining 3 armies from each side, with the last pairing being the remaining armies.")
    print("-" * 100)
    print("Ready?")
    ready = mv.boolean_validation("Enter yes/y or no/n: ")
    if not ready:
        while not ready:
            print("No worries. Take your time to read the explanation.")
            ready = mv.boolean_validation("Enter yes/y when ready: ")

def display_matrix(df: pd.DataFrame, prompt: str = None) -> None:
    if prompt != None:
        print(prompt)
    print(df)

# UI sequence for first round of matchups
def round_one_selection(df: pd.DataFrame, ally_dict: dict, enemy_dict: dict, ally_set: set, enemy_set: set, factions: list[str], enemy_armies: list[str], randomize: bool) -> tuple[list[tuple[int, int]], int]:
    m_m_and_std = pd.concat([df.mean(axis=1).to_frame(name="Mean Differential"), df.median(axis=1).to_frame(name="Median Differential"), df.std(axis=1).to_frame(name="Standard Deviation")], axis=1)
    display_matrix(m_m_and_std, "\nMean, Median, and Standard Deviation: ")
    # maximum path selection logic will be implemented in the maximum_path function in the maximum_path.py file.
    best_total = mp.maximum_path(df)
    print("-" * 100)

    print("\nStep 1: Selection of first army: ")
        
    ally = mv.team_validation("\nEnter the name of your first army: ", ally_dict, ally_set)
    if randomize:
        enemy_ran = random.choice(list(enemy_dict.keys()))
        enemy = enemy_dict[enemy_ran]
        print(f"Randomly selected enemy army: {enemy_armies[enemy]}")
        enemy_set.add(enemy_armies[enemy])
    else:
        enemy = mv.team_validation("Enter the name of the enemy's first army: ", enemy_dict, enemy_set)

    print("\nStep 2: Select 2 army options for the opposing team to choose from.")
    print("        Once both teams have selected, teams will reveal their selections.")

    progress = mv.boolean_validation("\nHave you selected your 2 armies? (yes/y or no/n): ")
    while not progress:
        print("Please select your 2 armies and then continue.")
        progress = mv.boolean_validation("\nHave you selected your 2 armies? (yes/y or no/n): ")

    ally_options = []
    while len(ally_options) < 2:
        ally_option = mv.string_validation(f"Enter the name of your army option {len(ally_options) + 1}: ")
        if (ally_option in ally_dict) and not (ally_option in ally_options):
            ally_options.append(ally_option)
        else:
            print(f"Invalid input. {ally_option} is not a valid army or has already been selected.")
            
    if randomize:
        enemy_options = random.sample(list(set(enemy_dict.keys()) - enemy_set), 2)
        print(f"\nRandomly selected enemy armies: {enemy_options[0]} and {enemy_options[1]}")
    else:
        enemy_options = []
        print()
        while len(enemy_options) < 2:
            enemy_option = mv.string_validation(f"Enter the name of the enemy's army option {len(enemy_options) + 1}: ")
            if (enemy_option in enemy_dict) and not (enemy_option in enemy_options) and not (enemy_option in enemy_set):
                enemy_options.append(enemy_option)
            else:
                print(f"Invalid input. {enemy_option} is not a valid army or has already been selected.")

    print("\nStep 3: Select which of the 2 enemy armies will go against your first army.")
    print("        The opposing team will select the army that will go against their first army.")

    progress = False
    while not progress:
        enemy_select = mv.string_validation(f"\nEnter the name of the enemy's army that will play against your {factions[ally]}: ")
        if enemy_select in enemy_options:
            progress = True
            enemy_set.add(enemy_select)
            enemy_matchup = enemy_dict[enemy_select]
        else:
            print(f"Invalid input. {enemy_select} is not one of the selected enemy armies: {enemy_options}")

    if randomize:
        ally_ran = random.choice(ally_options)
        print(f"Randomly selected ally matchup: {ally_ran}")
        ally_set.add(ally_ran)
        ally_matchup = ally_dict[ally_ran]
    else:
        ally_matchup = mv.team_validation(f"Enter the name of your team's army that will play against the enemy's {enemy_armies[enemy]}: ", ally_dict, ally_set)
    
    match_list = [(ally, enemy_matchup), (ally_matchup, enemy)]
    return match_list, best_total

# UI sequence for second round of matchups
def round_two_selection(df_copy: pd.DataFrame, ally_dict: dict, enemy_dict: dict, ally_set: set, enemy_set: set, factions: list[str], enemy_armies: list[str], current_total: int, randomize: bool) -> tuple[list[tuple[int, int]], int]:
    print()
    print("-" * 100)
    display_matrix(df_copy, "\nUpdated Matchup Matrix: ")

    round_two_total = mp.maximum_path(df_copy, current_total)
    print("-" * 100)

    print("\nStep 4: Select army to present to the opposing team: ")
    print("        Final two armies will be presented as selections for the opposing team to choose from.")

    ally = mv.team_validation("\nEnter the name of your next army: ", ally_dict, ally_set)
    if randomize:
        enemy_ran = random.choice(list(set(enemy_dict.keys()) - enemy_set))
        enemy = enemy_dict[enemy_ran]
        print(f"Randomly selected enemy army: {enemy_armies[enemy]}")
        enemy_set.add(enemy_armies[enemy])
    else:
        enemy = mv.team_validation("Enter the name of the enemy's next army: ", enemy_dict, enemy_set)

    print("\nStep 5: Final two armies are presented as selections. Select which army will face yours.")
    print("        The final two armies will play against each other.")
    print("Remaining Allies: ")
    for ally_army in list(set(ally_dict.keys()) - ally_set):
        print(f"- {ally_army}")
    print("Remaining Enemies: ")
    for enemy_army in list(set(enemy_dict.keys()) - enemy_set):
        print(f"- {enemy_army}")

    enemy_matchup = mv.team_validation(f"\nEnter the name of the enemy's army that will play against your {factions[ally]}: ", enemy_dict, enemy_set)
    if randomize:
        ally_ran = random.choice(list(set(ally_dict.keys()) - ally_set))
        print(f"Randomly selected ally matchup: {ally_ran}")
        ally_set.add(ally_ran)
        ally_matchup = ally_dict[ally_ran]
    else:
        ally_matchup = mv.team_validation(f"Enter the name of your team's army that will play against the enemy's {enemy_armies[enemy]}: ", ally_dict, ally_set)

    match_list = [(ally, enemy_matchup), (ally_matchup, enemy)]

    last_ally = (set(ally_dict.keys()) - ally_set).pop()
    last_enemy = (set(enemy_dict.keys()) - enemy_set).pop()
    match_list.append((ally_dict[last_ally], enemy_dict[last_enemy]))
    return match_list, round_two_total

# display of final pairings and differentials
def final_pairings(match_list: list[tuple[int, int]], factions: list[str], enemy_armies: list[str], df: pd.DataFrame, best_total: int, round_two_total: int) -> None:
    print()
    print("-" * 100)
    print("\nFinal Pairings w/ Estimated Differentials: \n")
    sum_differential = 0

    for i, (ally, enemy) in enumerate(match_list):
        print(f"Match {i + 1}: {factions[ally]} vs {enemy_armies[enemy]} \n- Estimated Differential: {df.at[factions[ally], enemy_armies[enemy]]}")
        sum_differential += df.at[factions[ally], enemy_armies[enemy]]
    print(f"\nFinal Estimated Differential: {sum_differential}")
    print(f"Best Total Differential: {best_total} - Difference from Final: {best_total - sum_differential}")
    print(f"Round Two Total Differential: {round_two_total} - Difference from Final: {round_two_total - sum_differential}")

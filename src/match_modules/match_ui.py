import pandas as pd
from match_modules import match_validation as mv
from match_modules import maximum_path as mp

# Display functions
def starting_display() -> None:

    print("\nWelcome to the AoS Teams Matchup Program.")
    print("This program will aid in the analysis of ideal matchups for a 5v5 Tournament.")

    print("\nBefore starting, ensure that map_name fields are consistent in order and tense across all teams in the JSON file.")
    print("This is important to ensure that the correct matchup matrix is pulled for each team and map combination.")

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
    print("These metrics include mean pairings differential, pairings standard deviation, and ideal pairings based on a maximum bipartite matching algorithm.")
    print("The data analyzed is based on differential estimation matrices for each team and map combination, which are stored in a JSON file.")
    print("-" * 100)
    print("Step 1: Each team selects an army to present to the opposing team.")
    print("Step 2: Both teams then reveal their armies")
    print("Step 3: Teams select 2 armies as potential matchups for the presented army.")
    print("Step 4: Teams then select which of the 2 armies they want their initial army to go against.")
    print("This process is repeated with the remaining 3 armies from each side, with the last pairing being the remaining armies.")
    print("-" * 100)
    print("Ready?")
    ready = mv.boolean_validation("Enter yes/y or no/n: ")
    if ready:
        print("Great! Let's get started.")
    else:
        while not ready:
            print("No worries. Take your time to read the explanation.")
            ready = mv.boolean_validation("Enter yes/y when ready: ")

def display_matrix(prompt: str, df: pd.DataFrame) -> None:
    print(prompt)
    print(df)

def round_one_selection(df: pd.DataFrame, ally_dict: dict, enemy_dict: dict, ally_set: set, enemy_set: set, factions: list[str], enemy_armies: list[str]) -> list[tuple[int, int]]:
    start = mv.boolean_validation("\nWould you like to start the analysis for round 1 selection? (yes/y or no/n): ")
    while not start:
        print("Program is paused.")
        start = mv.boolean_validation("Enter yes/y when ready to proceed: ")
    # maximum path selection logic will be implemented in the maximum_path function in the maximum_path.py file.
    mp.maximum_path(df)

    print("\nStep 1: Selection of first army: ")
    print("Recommended: Select an army with a high mean differential and low standard deviation.")
    print("             It is also recommeneded to save an army with similar metrics for last matchup to avoid a large negative differential.")
    mean_and_std = pd.concat([df.mean(axis=1).to_frame(name="Mean Differential"), df.std(axis=1).to_frame(name="Standard Deviation")], axis=1)
    display_matrix("\nMatchup Metrics: ", mean_and_std)
        
    ally = mv.team_validation("Enter the name of your first army: ", ally_dict, ally_set)
    enemy = mv.team_validation("Enter the name of the enemy's first army: ", enemy_dict, enemy_set)

    print("\nStep 2: Select 2 army options for the opposing team to choose from.")
    print("\nStep 3: Select the army that will go against your first army.")
    print("        The opposing team will select the army that will go against their first army.")

    enemy_matchup = mv.team_validation(f"\nEnter the name of the enemy's army that will play against your {factions[ally]}: ", enemy_dict, enemy_set)
    ally_matchup = mv.team_validation(f"Enter the name of your team's army that will play against the enemy's {enemy_armies[enemy]}: ", ally_dict, ally_set)

    match_list = [(ally, enemy_matchup), (ally_matchup, enemy)]
    return match_list

def round_two_selection(df_copy: pd.DataFrame, ally_dict: dict, enemy_dict: dict, ally_set: set, enemy_set: set, factions: list[str], enemy_armies: list[str]) -> list[tuple[int, int]]:
    display_matrix("\nUpdated Matchup Matrix: ", df_copy)
    print("\nStep 4: Selection of third army: ")
    print("        3 armies remain for each team. Select an army to present to the opposing team.")
    print("        The final remaining armies will be the last matchup.")

    ally = mv.team_validation("\nEnter the name of your next army: ", ally_dict, ally_set)
    enemy = mv.team_validation("Enter the name of the enemy's next army: ", enemy_dict, enemy_set)

    print("\nStep 5: Select the army that will go against your second army.")
    print("        The opposing team will select the army that will go against their second army.")

    enemy_matchup = mv.team_validation(f"Enter the name of the enemy's army that will play against your {factions[ally]}: ", enemy_dict, enemy_set)
    ally_matchup = mv.team_validation(f"Enter the name of your team's army that will play against the enemy's {enemy_armies[enemy]}: ", ally_dict, ally_set)

    match_list = [(ally, enemy_matchup), (ally_matchup, enemy)]

    last_ally = (set(ally_dict.keys()) - ally_set).pop()
    last_enemy = (set(enemy_dict.keys()) - enemy_set).pop()
    match_list.append((ally_dict[last_ally], enemy_dict[last_enemy]))
    return match_list

def final_pairings(match_list: list[tuple[int, int]], factions: list[str], enemy_armies: list[str], df: pd.DataFrame) -> None:
    print("\nFinal Pairings w/ Estimated Differentials: ")
    sum_differential = None

    for i, (ally, enemy) in enumerate(match_list):
        print(f"Match {i + 1}: {factions[ally]} vs {enemy_armies[enemy]} \n- Estimated Differential: {df.at[factions[ally], enemy_armies[enemy]]}")
        sum_differential = df.at[factions[ally], enemy_armies[enemy]] if sum_differential is None else sum_differential + df.at[factions[ally], enemy_armies[enemy]]
    print(f"Total Estimated Differential: {sum_differential}")

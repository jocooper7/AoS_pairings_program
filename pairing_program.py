# Age of Sigmar Teams Matchup Program

# imports
import pandas as pd
import json
import numpy as np

# Validation and base functions
def int_validation(prompt: str, min_value: int, max_value: int) -> int:
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Invalid input. Please enter an integer between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def boolean_validation(prompt: str) -> bool:
    while True:
        value = input(prompt).strip().lower()
        if value in ['yes', 'y']:
            return True
        elif value in ['no', 'n']:
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

# Base Variables and Lists
team_members = ["Adam", "Brian", "Jo", "Shane", "E"]
factions = ["Soulblight Gravelords", "Seraphon", "Maggotkin of Nurgle", "Disciples of Tzeench", "Skaven"]

enemy_teams = ["Corsairs", "A House of Villains", "Llama Boyz", "Miscasts", "TSD", "TSD2(GG)"]
maps_options = ["Surge of Slaughter", "Lifecycle", "Cyclic Shifts", "Passing Seasons", "Grasp of Thorns"]

# Accessing the JSON file and creating a DataFrame
def create_dataframe(opponent_team: str, selected_map: str) -> pd.DataFrame:
    with open("matchup_doc.json") as file:
        data = json.load(file)

    team = next(t for t in data if t["team_name"] == opponent_team)
    matrix = next(m["matrix"] for m in team["maps"] if m["map_name"] == selected_map)

    df = pd.DataFrame(matrix, index=pd.MultiIndex.from_arrays([team_members, factions], names=["Team Members", "Factions"]), columns=team["enemy_factions"])
    return df

# Display functions
def display_welcome() -> None:
    print()
    print("Welcome to the AoS Teams Matchup Program.")
    print("This program will aid in the analysis of ideal matchups for a 5v5 Tournament.")
    print()
    print("Would you like an explanation of the pairings minigame?")
    print("If yes, an explanation will be provided, if no, the program will continue to the matchup selection.")

def display_team_selection() -> None:
    print()
    print("Enemy team options: ")
    for i, team in enumerate(enemy_teams):
        print(f"{i}. {team}")

def display_map_selection() -> None:
    print()
    print("Map options: ")
    for i, map_option in enumerate(maps_options):
        print(f"{i}. {map_option}")

def explanation_display() -> None:
    print()
    print("While Age of Sigmar is typically a 1v1 game, there are special 5v5 tournaments.")
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
    ready = boolean_validation("Enter yes/y or no/n: ")
    if ready:
        print("Great! Let's get started.")
    else:
        while not ready:
            print("No worries. Take your time to read the explanation.")
            ready = boolean_validation("Enter yes/y when ready: ")


# Program Driver
def run_program():

    # Initial greeting and setup
    display_welcome()
    start = False
    while not start: 
        explain = boolean_validation("Enter yes/y or no/n: ")

        if explain:
            explanation_display()
        start = True

    ready = False
    while not ready:
        display_team_selection()
        enemy_selection = int_validation("Select Number (press Enter to continue): ", 0, len(enemy_teams) - 1)
        display_map_selection()
        map_selection = int_validation("Select Number (press Enter to continue): ", 0, len(maps_options) - 1)
        print()
        print(f"You selected enemy team: {enemy_teams[enemy_selection]}, and map: {maps_options[map_selection]}.")
        ready = boolean_validation("Is this correct? (yes/y or no/n): ")

    # Create DataFrame from JSON file and selections
    # NOTE: The JSON file's matrices are currently filled with randomized differentials for testing purposes. The actual data will be filled in later.
    opponent_team = enemy_teams[enemy_selection]
    selected_map = maps_options[map_selection]
    df = create_dataframe(opponent_team, selected_map)
    print()
    print("Matchup Differential Matrix:")
    print(df)

if __name__ == "__main__":
    run_program()
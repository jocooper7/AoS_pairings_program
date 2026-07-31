# Age of Sigmar Teams Matchup Program

# imports
import pandas as pd
import json
import numpy as np

# Base Variables and Lists
default_team_members = ["Adam", "Brian", "Jo", "Shane", "E"]
default_factions = ["Soulblight Gravelords", "Seraphon", "Maggotkin of Nurgle", "Disciples of Tzeentch", "Skaven"]

# Map Options:
# "Passing Seasons", "Paths of the Fey", "Roiling Roots", "Cyclic Shifts"
# "Surge of Slaughter", "Linked Ley Lines", "Noxious Nexus", "The Liferoots"
# "Bountiful Equinox", "Lifecycle", "Creeping Corruption","Grasp of Thorns"

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

def string_validation(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if len(value) > 30:
            print("Invalid input. Please enter a string with 30 characters or fewer.")
        elif value:
            return value
        else:
            print("Invalid input. Please enter a non-empty string.")

# Accessing the JSON file and creating a DataFrame
def create_dataframe(team_members: list, factions: list, opponent_team: str, selected_map: str) -> pd.DataFrame:
    try:
        with open("matchup_doc.json") as file:
            data = json.load(file)

        team = next(t for t in data if t["team_name"] == opponent_team)
        matrix = next(m["matrix"] for m in team["maps"] if m["map_name"] == selected_map)
        df = pd.DataFrame(matrix, index=pd.MultiIndex.from_arrays([team_members, factions], names=["Team Members", "Factions"]), columns=team["enemy_factions"])
        return df
    except FileNotFoundError:
        print("Error: matchup_doc.json file not found.")
        exit(1)
    except json.JSONDecodeError:
        print("Error: JSON file is not properly formatted.")
        exit(1)
    except StopIteration:
        print(f"Error: Could not find data for map '{selected_map}'.")
        print("Please check the JSON file and ensure the data is correct.")
        print("Ensure the map_name field matches in order and tense across all teams in the JSON file.")
        exit(1)

# Display functions
def starting_display() -> None:
    print()
    print("Welcome to the AoS Teams Matchup Program.")
    print("This program will aid in the analysis of ideal matchups for a 5v5 Tournament.")
    print()
    print("Before starting, ensure that map_name fields are consistent in order and tense across all teams in the JSON file.")
    print("This is important to ensure that the correct matchup matrix is pulled for each team and map combination.")
    print()
    print("Would you like an explanation of the pairings minigame?")
    print("If yes, an explanation will be provided. If no, the program will continue to the matchup selection.")
    start = False
    while not start: 
        explain = boolean_validation("Enter yes/y or no/n: ")

        if explain:
            explanation_display()
        start = True

def display_team_selection(enemy_list) -> None:
    print()
    print("Enemy team options: ")
    for i, team in enumerate(enemy_list):
        print(f"{i + 1}. {team}")

def display_map_selection(maps_list) -> None:
    print()
    print("Map options: ")
    for i, map_option in enumerate(maps_list):
        print(f"{i + 1}. {map_option}")

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

def display_matrix(prompt: str, df: pd.DataFrame) -> None:
    print()
    print(prompt)
    print(df)

# Functions to change team members, factions, and maps
def change_team_and_factions() -> list:
    print()
    for i in range(len(default_team_members)):
        print(f"Current team member {i+1}: {default_team_members[i]} playing {default_factions[i]}")
        name = string_validation(f"Enter new name for team member {i+1}: ")
        faction = string_validation(f"Enter new faction for team member {i+1}: ")
        default_team_members[i] = name
        default_factions[i] = faction
    return default_team_members, default_factions

def change_info() -> list:
    print()
    print("Would you like to change default team information?")
    change = boolean_validation("Enter yes/y or no/n: ")
    if change:
        print("Changing team members and factions.")
        team_members, factions = change_team_and_factions()
    else:
        print("No changes will be made to the default team information.")
        team_members, factions = default_team_members, default_factions
    print()
    return team_members, factions

def add_enemy_teams() -> list:
    try:
        with open("matchup_doc.json") as file:
            data = json.load(file)
            enemies = [team["team_name"] for team in data]
        return enemies
    except FileNotFoundError:
        print("Error: matchup_doc.json file not found.")
        print("Exiting program. Please ensure the file is in the correct directory and try again.")
        exit(1)
    except json.JSONDecodeError:
        print("Error: JSON file is not properly formatted.")
        print("Exiting program. Please check the file format and try again.")
        exit(1)

def add_maps() -> list:
    try:
        with open("matchup_doc.json") as file:
            data = json.load(file)
            maps = list({map_info["map_name"] for team in data for map_info in team["maps"]})
        return maps
    except FileNotFoundError:
        print("Error: matchup_doc.json file not found.")
        print("Exiting program. Please ensure the file is in the correct directory and try again.")
        exit(1)
    except json.JSONDecodeError:
        print("Error: JSON file is not properly formatted.")
        print("Exiting program. Please check the file format and try again.")
        exit(1)

def matchup_selection(enemy_list, maps_list) -> tuple[int, int]:
    ready = False
    while not ready:
        display_team_selection(enemy_list)
        enemy = int_validation("Select Number (press Enter to continue): ", 1, len(enemy_list))
        display_map_selection(maps_list)
        map_num = int_validation("Select Number (press Enter to continue): ", 1, len(maps_list))
        print()
        print(f"You selected enemy team: {enemy_list[enemy - 1]} and map: {maps_list[map_num - 1]}.")
        ready = boolean_validation("Is this correct? (yes/y or no/n): ")
    return enemy - 1, map_num - 1

# Program Driver
def run_program():

    # Initial greeting and setup
    starting_display()

    # allows user to change user team info (members and armies) if needed.
    team_members, factions = change_info()
        
    # pulls team name data from JSON file and creates a list of enemy teams for selection.
    enemy_teams = add_enemy_teams()
    map_options = add_maps()

    enemy_selection, map_selection = matchup_selection(enemy_teams, map_options)

    # Create DataFrame from JSON file and selections
    # NOTE: The JSON file's matrices are currently filled with randomized differentials for testing purposes. 
    df = create_dataframe(team_members, factions, enemy_teams[enemy_selection], map_options[map_selection])
    display_matrix("Differential Matrix Display: ",df)

    print()
    mean_and_std = pd.concat([df.mean(axis=1).to_frame(name="Mean Differential"), df.std(axis=1).to_frame(name="Standard Deviation")], axis=1)
    display_matrix("Matchup Metrics: ", mean_and_std)

if __name__ == "__main__":
    run_program()
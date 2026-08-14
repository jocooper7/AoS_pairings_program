# Age of Sigmar Teams Matchup Program

# imports
import warnings
import pandas as pd
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
import json
import os

from match_modules import match_validation as mv
from match_modules import match_ui as mui

# Base Variables and Lists
default_factions = ["Soulblight Gravelords", "Seraphon", "Maggotkin of Nurgle", "Disciples of Tzeentch", "Skaven"]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(SCRIPT_DIR, "matchup_doc.json")

# Map Options:
# "Passing Seasons", "Paths of the Fey", "Roiling Roots", "Cyclic Shifts"
# "Surge of Slaughter", "Linked Ley Lines", "Noxious Nexus", "The Liferoots"
# "Bountiful Equinox", "Lifecycle", "Creeping Corruption","Grasp of Thorns"

# Accessing the JSON file and creating a DataFrame
def create_dataframe(factions: list, opponent_team: str, selected_map: str) -> pd.DataFrame:
    try:
        with open(JSON_PATH) as file:
            data = json.load(file)

        team = next(t for t in data if t["team_name"] == opponent_team)
        matrix = next(m["matrix"] for m in team["maps"] if m["map_name"] == selected_map)
        df = pd.DataFrame(matrix, index=pd.MultiIndex.from_arrays([factions], names=["Your Factions"]), columns=team["enemy_factions"])
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

# Functions to change team members, factions, and maps
def change_team_and_factions() -> list:
    print()
    for i in range(len(default_factions)):
        print(f"Current team member {i+1} playing {default_factions[i]}")
        faction = mv.string_validation(f"Enter new faction for team member {i+1}: ")
        default_factions[i] = faction
    return default_factions

def change_info() -> list:
    print("\nWould you like to change default team information?")
    change = mv.boolean_validation("Enter yes/y or no/n: ")
    if change:
        print("Changing factions.")
        factions = change_team_and_factions()
    else:
        print("No changes will be made to the default team information.")
        factions = default_factions
    print()
    return factions

def add_enemy_teams() -> list:
    try:
        with open(JSON_PATH) as file:
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
        with open(JSON_PATH) as file:
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
        mui.display_team_selection(enemy_list)
        enemy = mv.int_validation("Select Number (press Enter to continue): ", 1, len(enemy_list))
        mui.display_map_selection(maps_list)
        map_num = mv.int_validation("Select Number (press Enter to continue): ", 1, len(maps_list))
        print()
        print(f"You selected enemy team: {enemy_list[enemy - 1]} and map: {maps_list[map_num - 1]}.")
        ready = mv.boolean_validation("Is this correct? (yes/y or no/n): ")
    return enemy - 1, map_num - 1

# Program Driver
def run_program():

    print("Validating matchup_doc.json file...")
    valid = mv.json_file_validation(JSON_PATH)
    if not valid:
        print("Exiting program due to invalid JSON file.")
        exit(1)

    # Initial greeting and setup
    mui.starting_display()

    # allows user to change user team info (members and armies) if needed.
    factions = change_info()
        
    # pulls team name data from JSON file and creates a list of enemy teams for selection.
    enemy_teams = add_enemy_teams()
    map_options = add_maps()

    enemy_selection, map_selection = matchup_selection(enemy_teams, map_options)

    # Create DataFrame from JSON file and selections
    # NOTE: The JSON file's matrices are currently filled with randomized differentials for testing purposes. 
    df = create_dataframe(factions, enemy_teams[enemy_selection], map_options[map_selection])
    df.index = df.index.get_level_values(0)
    enemy_armies = df.columns.tolist()
    enemy_dict = {}
    for i, army in enumerate(enemy_armies):
        enemy_dict[army] = i
    enemy_set = set()

    ally_dict = {}
    for i, army in enumerate(factions):
        ally_dict[army] = i
    ally_set = set()

    mui.display_matrix("Differential Matrix Display: ", df)

    match_list = []
    match_list.extend(mui.round_one_selection(df, ally_dict, enemy_dict, ally_set, enemy_set, factions, enemy_armies))
    ally_one, enemy_one = match_list[0]
    ally_two, enemy_two = match_list[1]

    df_copy = df.drop(index=[factions[ally_one], factions[ally_two]])
    df_copy = df_copy.drop(columns=[enemy_armies[enemy_one], enemy_armies[enemy_two]])

    match_list.extend(mui.round_two_selection(df_copy, ally_dict, enemy_dict, ally_set, enemy_set, factions, enemy_armies))

    print(df)

    mui.final_pairings(match_list, factions, enemy_armies, df)

    print("\nProgram completed. Thank you for using the Age of Sigmar Teams Matchup Program!\n")

if __name__ == "__main__":
    run_program()
import json
from jsonschema import validate, ValidationError


# schema creation for validation 
valid_schema = {
    "$schema": "https://json-schema.org",
    "title": "FactionMatrixData",
    "type": "array",
    "minItems": 1,
    "items": {
        "type": "object",
        "required": ["team_name", "enemy_factions", "maps"],
        "additionalProperties": False, 
        "properties": {
            "team_name": {
                "type": "string"
            },
            "enemy_factions": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "maps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["map_name", "matrix"],
                    "additionalProperties": False,  
                    "properties": {
                        "map_name": {
                            "type": "string"
                        },
                        "matrix": {
                            "type": "array",
                            "minItems": 5,
                            "maxItems": 5,
                            "items": {
                                "type": "array",
                                "minItems": 5,
                                "maxItems": 5,
                                "items": {
                                    "type": "integer"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}


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

def json_file_validation(file_path: str) -> bool:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            validate(instance = data, schema = valid_schema)
        return True
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"Invalid JSON file: {e}")
        return False

def team_validation(prompt: str, curr_dict: dict, curr_set: set) -> int:
    while True:
                curr = string_validation(prompt)
                if curr in curr_dict:
                    if curr in curr_set:
                        print(f"Invalid input. {curr} has already been selected.")
                    else:
                        break
                else:
                    print(f"Invalid input. Please enter a valid army name from teams: {set(curr_dict.keys()) - curr_set}")
    curr_set.add(curr)
    ind = curr_dict[curr]
    return ind
    
    
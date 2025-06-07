import os
import json
import requests
from datetime import datetime

# Define the folder and file path
FOLDER_NAME = "json_files"
FILE_NAME = "jokes.json"
FILE_PATH = os.path.join(FOLDER_NAME, FILE_NAME)

# Create the directory if it doesn't exist
os.makedirs(FOLDER_NAME, exist_ok=True)

# --- Load existing jokes or initialize a new list ---
try:
    with open(FILE_PATH, 'r') as f:
        # Handle empty file case
        content = f.read()
        if not content:
            jokes_data = []
        else:
            jokes_data = json.loads(content)
except FileNotFoundError:
    jokes_data = []
except json.JSONDecodeError:
    print(f"Warning: Could not decode JSON from {FILE_PATH}. Starting with an empty list.")
    jokes_data = []


# --- Fetch a new joke from the API ---
try:
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    new_joke = response.json()

    # --- Determine the new ID ---
    if jokes_data:
        # Find the highest existing ID and add 1
        last_id = max(joke.get('ID', 0) for joke in jokes_data)
        new_id = last_id + 1
    else:
        # Start from 1 if no jokes exist
        new_id = 1

    # --- Prepare the new joke entry ---
    joke_to_save = {
        "ID": new_id,
        "timestamp": datetime.now().isoformat(),
        "type": new_joke.get("type"),
        "setup": new_joke.get("setup"),
        "punchline": new_joke.get("punchline")
    }

    # --- Append the new joke and save the file ---
    jokes_data.append(joke_to_save)

    with open(FILE_PATH, 'w') as f:
        json.dump(jokes_data, f, indent=4)

    print(f"Successfully fetched and saved a new joke to {FILE_PATH}")
    print(f"New joke added with ID: {new_id}")

except requests.exceptions.RequestException as e:
    print(f"Error fetching joke from API: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
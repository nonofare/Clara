import os
import json


def get_key(filepath: str, key_name: str) -> str:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")

        if key_name not in data:
            raise KeyError(f"Key '{key_name}' not found.")

        key = data[key_name]
        if not key:
            raise ValueError(f"Key '{key_name}' is empty.")

        return key


def get_persona(filepath: str) -> str:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r") as file:
        content = file.read()

    if not content:
        raise ValueError("File is empty.")

    return content

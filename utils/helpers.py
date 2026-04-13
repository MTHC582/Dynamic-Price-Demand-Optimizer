import json
import os

def load_config(filepath="data/config.json"):
    """Loads simulation parameters from the JSON config file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Error: Config file not found at {filepath}")
    
    with open(filepath, 'r') as file:
        config = json.load(file)
        
    print("[Config loaded successfully]")
    return config

# Quick test block (runs only if you execute this specific file)
if __name__ == "__main__":
    conf = load_config()
    print(conf)

import os
import json

# Wherever this file is executed, a settings.json will be created there
# Ideally, this will be put in the home directory
SETTINGS_FILENAME = "settings.json"
SETTINGS_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.join(SETTINGS_DIRECTORY, SETTINGS_FILENAME)

DEFAULT_SETTINGS = {
    "syringeDiameter" : 21.0,
    "stepsPerMm" : 4063.89474,
    "showSteps" : False,
    "defaultFlowRate" : 100.0,
    "directControlSpeed" : 0.5,
    "discoveryqHostname" : "ivmx-discovery3.local",
    "networkMode" : "Eduroam",
    "colorTheme" : "System"
}

# ========================
# Function Implementations
# ========================


def getAllSettings() -> dict:
    # Create settings.json if it doesn't already exist
    if not os.path.exists(SETTINGS_PATH):
        print("No settings file found, generating now")
        resetSettings()
    
    # Overwrite settings.json if it is malformed
    with open(SETTINGS_PATH, "r") as jsonfp:
        try:
            json.load(jsonfp)
        except json.JSONDecodeError:
            print("Settings file malformed, regenerating")
            resetSettings()
    
    with open(SETTINGS_PATH, "r") as jsonfp:
        return json.load(jsonfp)

def getSetting(key: str):
    return getAllSettings().get(key)

def setSetting(key: str, value: any):
    newSettings = getAllSettings()
    newSettings[key] = value
    
    with open(SETTINGS_PATH, "w") as jsonfp:
        json.dump(newSettings, jsonfp)

def setAllSettings(newSettings: any):
    with open(SETTINGS_PATH, "w") as jsonfp:
        json.dump(newSettings, jsonfp)

def resetSettings():
    with open(SETTINGS_PATH, "w") as jsonfp:
        json.dump(DEFAULT_SETTINGS, jsonfp)


# ==============
# On module load
# ==============

# This will call all necessary facilities to create the settings file if it doesn't already exist
getAllSettings()

print(f"Settings loaded from {SETTINGS_PATH}")

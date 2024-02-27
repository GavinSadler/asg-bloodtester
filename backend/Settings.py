
import os
import json

# Wherever this file is executed, a settings.json will be created there
SETTINGS_PATH = "./settings.json"

DEFAULT_SETTINGS = {
    "syringeDiameter" : 21,
    "defaultFlowRate" : 50.0,
    "maxFlowRate" : 150.0,
    "discoveryqHostname" : "ivmx-discovery3.local",
    "networkMode" : "Eduroam"
}

# ========================
# Function Implementations
# ========================


def getAllSettings() -> dict:
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


# Create settings.json if it doesn't already exist
if not os.path.exists(SETTINGS_PATH):
    resetSettings()

# Overwrite settings.json if it is malformed
with open(SETTINGS_PATH, "r") as jsonfp:
    try:
        json.load(jsonfp)
    except json.JSONDecodeError:
        resetSettings()

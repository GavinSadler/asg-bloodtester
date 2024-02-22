import json
import os
import platform
import subprocess

import Constants
import DummyData
import requests
import Settings
from flask import Flask, Response, jsonify, request
from flask_cors import CORS

# If we are testing locally, these will not be able to import
try:
    import MotorController
    import SyringeController

    motor = MotorController.MotorController()
    syringe = SyringeController.Syringe(motor, Constants.STEPS_PER_mL)
except:
    print("Unable to load motorController and/or syringeController")

app = Flask(__name__)
cors = CORS(app)


# =================
# General endpoints
# =================


@app.route("/")
def root():
    return "Backend running"


@app.route("/networkinfo")
def networkinfo():

    plat = platform.platform().lower()

    if "windows" in plat:
        return {"output" : subprocess.check_output(["ipconfig"])}
    elif "linux" in plat:
        return {"output" : subprocess.check_output(["nmcli"])}

    return {"error": "unable to grab network information, error parsing platform information"}, 500


@app.route("/settings", methods=["GET", "POST"])
def settings():

    #Overwrite settings if it is a post request
    if request.method == "POST":

        jsonData: dict = request.get_json()

        Settings.setAllSettings(jsonData)

    return Settings.getAllSettings()

@app.route("/resetSettings")
def resetSettings():
    Settings.resetSettings()
    
    return {}


# ============================
# Syringe controller endpoints
# ============================


@app.route("/dispense")
def dispense():
    amount = request.args.get("amount", "-1")

    try:
        amount = float(amount)
    except ValueError:
        return {"error": f"could not parse float from argument amount ({amount})"}, 400

    if amount < 0:
        return {"error": f"argument amount was negative ({amount}) or not supplied"}, 400

    syringe.dispense(amount)

    return {"dispenseAmount": amount, "unit" : "mL"}


@app.route("/retract")
def retract():
    amount = request.args.get("amount", "-1")

    try:
        amount = float(amount)
    except ValueError:
        return {"error": f"could not parse float from argument amount ({amount})"}, 400

    if amount < 0:
        return {"error": f"argument amount was negative ({amount}) or not supplied"}, 400

    syringe.retract(amount)

    return {"retractAmount": amount, "unit" : "mL"}

@app.route("/dispenseContinuous")
def dispenseContinuous():
    syringe.dispenseContinuous()
    return {}

@app.route("/retractContinuous")
def retractContinuous():
    syringe.retractContinuous()
    return {}

@app.route("/stop")
def stop():
    motor.stop()
    return {}

@app.route("/setDispenseSpeed")
def setDispenseSpeed():
    speed = request.args.get("speed", "-1")

    try:
        speed = float(speed)
    except ValueError:
        return {"error": f"could not parse float from argument speed ({speed})"}, 400

    if speed <= 0:
        return {"error": f"argument speed was negative ({speed}) or not supplied"}, 400

    syringe.setDispenseSpeed(speed)

    return {"dispenseSpeed": speed}

@app.route("/getSteps")
def getSteps():
    return {"steps" : motor.getSteps()}


# =====================
# Discovery Q proxy
# =====================


@app.route("/php/DAQControl.php")
def DAQControl():
    # TODO: Call Discovery Q's endpoint and return data back to caller
    return "Not yet implemented", 501


# TODO: Investigate direct access to the DB instead of through HTTP enpoint
@app.route("/php/mysql2json.php")
def mysql2json():
    database = ""
    table = ""

    try:
        database = str(request.args.get("database"))
        table = str(request.args.get("table"))
    except TypeError:
        return f"Error, missing input parameter(s).", 500
    except ValueError:
        return f"Error, could not parse integer from input parameter(s).", 500

    if (
        request.args.get("debug") == "true"
        and database == "View"
        and table == "temperature_recent"
    ):
        return DummyData.MYSQL2JSON_PHP_RESPONSE

    res = requests.get(Constants.DISCOVERY_NAME + request.full_path)

    return res.content, res.status_code, res.headers.items()



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

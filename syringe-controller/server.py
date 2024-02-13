
from flask import Flask, request

import constants
import dummyData
# import syringeController
# import motorController

# motor = motorController.MotorController()
# syringe = syringeController.Syringe(motor, constants.STEPS_PER_mL)

app = Flask(__name__)

@app.route("/")
def root():
    return "Backend running"

# ============================
# Syringe controller endpoints
# ============================

@app.route("/dispense")
def dispense():
    amount = request.args.get("amount", "-1")
    
    try:
        amount = float(amount)
    except ValueError:
        return "Usage: /dispense?amount=x, where x: float >= 0", 400
    
    if amount < 0:
        return "Usage: /dispense?amount=x, where x: float >= 0", 400
    
    syringe.dispense(amount)
    
    return f"Success, dispensing {amount}mL"

@app.route("/stop")
def stop():
    motor.stop()
    return "Success"
    
@app.route("/dispenseContinuous")
def dispenseContinuous():
    syringe.dispenseContinuous()
    return "Success"
    
@app.route("/retractContinuous")
def retractContinuous():
    syringe.retractContinuous()
    return "Success"

@app.route("/setDispenseSpeed")
def setDispenseSpeed():
    speed = request.args.get("speed", "-1")
    
    try:
        speed = float(speed)
    except ValueError:
        return "Usage: /setDispenseSpeed?speed=x, where x: float > 0", 400
    
    if speed <= 0:
            return "Usage: /setDispenseSpeed?speed=x, where x: float > 0", 400
    
    syringe.setDispenseSpeed(speed)
    
    return f"Success, dispense speed set to {speed}mL/min"

# =====================
# Discovery Q endpoints
# =====================

# NOTE: These routes forward to the routes provided by the Discovery Q
#       We can't make HTTP requests directly to the Discovery Q since it doesn't permit CORS requests

@app.route("/php/LastAcquisitionID.php")
def lastAcquisitionID():
    
    if (request.args.get('debug') == "true"):
        return '{"id":"600","sweep_mode":"1"}'
    
    # TODO: Call Discovery Q's endpoint and return data back to caller
    return 'Not yet implemented', 501

@app.route("/php/ChannelData.php")
def channelData():
    id = 0
    timestamp_min = 0
    timestamp_nth = 0
    device = 0
    well = 0
    
    try:
        id = int(request.args.get('id'))
        timestamp_min = int(request.args.get('timestamp_min'))
        timestamp_nth = int(request.args.get('timestamp_nth'))
        device = int(request.args.get('device'))
        well = int(request.args.get('well'))
    except TypeError:
        return f"Error, missing input parameter(s).", 500
    except ValueError:
        return f"Error, could not parse integer from input parameter(s).", 500
    
    if request.args.get('debug') == "true" and id == 600 and timestamp_min == 0 and timestamp_nth == 1 and device == 0 and well == 0:
        return dummyData.CHANNELDATA_PHP_RESPONSE
    
    # TODO: Call Discovery Q's endpoint and return data back to caller
    return 'Not yet implemented', 501

@app.route("/php/DAQControl.php")
def DAQControl():
    # TODO: Call Discovery Q's endpoint and return data back to caller
    return 'Not yet implemented', 501

# TODO: Investigate direct access to the DB instead of through HTTP enpoint
@app.route("/php/mysql2json.php")
def mysql2json():
    database = ""
    table = ""
    
    try:
        database = str(request.args.get('database'))
        table = str(request.args.get('table'))
    except TypeError:
        return f"Error, missing input parameter(s).", 500
    except ValueError:
        return f"Error, could not parse integer from input parameter(s).", 500

    if request.args.get('debug') == "true" and database == "View" and table == "temperature_recent":
        return dummyData.MYSQL2JSON_PHP_RESPONSE
    
    # TODO: Call Discovery Q's endpoint and return data back to caller
    return 'Not yet implemented', 501

if __name__ == "__main__":
    app.run(port=5000, debug=True)

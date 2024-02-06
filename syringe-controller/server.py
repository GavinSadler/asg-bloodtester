
from flask import Flask, request
from constants import STEPS_PER_mL

from syringeController import Syringe
from motorController import MotorController

motor = MotorController()
syringe = Syringe(motor, STEPS_PER_mL)

app = Flask(__name__)

@app.route("/")
def root():
    return "Backend running"

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

if __name__ == "__main__":
    app.run(port=5000, debug=True)

import argparse

import netifaces
import requests
import Settings
from flask import Flask, Response, request, send_from_directory
from flask_cors import CORS

# If we are testing locally, these will not be able to import
try:
    import MotorController
    import SyringeController

    motor = MotorController.MotorController()
    syringe = SyringeController.Syringe(motor, float(Settings.getSetting("syringeDiameter")), float(Settings.getSetting("stepsPerMm")))
except Exception as e:
    print("Unable to load motorController and/or syringeController: ", e)

app = Flask(__name__, static_folder="../dist/assets", static_url_path="/assets")
cors = CORS(app)


# =================
# General endpoints
# =================


@app.route("/")
def serve_index():
    return send_from_directory("../dist", "index.html")


# This route is to serve static files from assets folder
@app.route("/assets/<path:path>")
def serve_static(path):
    return send_from_directory("../dist/assets", path)


@app.route("/networkinfo")
def networkinfo():

    return netifaces.ifaddresses("wlan0")[2][0]["addr"]


@app.route("/settings", methods=["GET", "POST"])
def settings():

    # Overwrite settings if it is a post request
    if request.method == "POST":
        Settings.setAllSettings(request.get_json())

        # Make sure to apply changes to the SyringeController object
        syringe.setDiameter(float(Settings.getSetting("syringeDiameter")) * 10 ** (-3))

        # And apply changes to any network devices

    return Settings.getAllSettings()


@app.route("/resetSettings")
def resetSettings():
    Settings.resetSettings()
    return Settings.getAllSettings()


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

    return {"dispenseAmount": amount, "unit": "mL"}


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

    return {"retractAmount": amount, "unit": "mL"}


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


@app.route("/setCarriageSpeed")
def setCarriageSpeed():
    speed = request.args.get("speed", "-1")

    try:
        speed = float(speed)
    except ValueError:
        return {"error": f"could not parse float from argument speed ({speed})"}, 400

    if speed <= 0:
        return {"error": f"argument speed was negative ({speed}) or not supplied"}, 400

    syringe.setCarriageSpeed(speed)

    return {"carriageSpeed": speed}


@app.route("/getSteps")
def getSteps():
    return str(motor.getSteps())


# =====================
# Discovery Q proxy
# =====================


# See https://stackoverflow.com/a/36601467 for an explanation of this proxy
@app.route("/discoveryqproxy/", defaults={"subpath": ""}, methods=["GET", "POST"])
@app.route("/discoveryqproxy/<path:subpath>", methods=["GET", "POST"])
def forwaredRequest(subpath):

    # Constrcut the new proxied URL
    discoveryQHostname = Settings.getSetting("discoveryqHostname")
    proxyUrl = request.url.replace(request.host, discoveryQHostname)
    proxyUrl = proxyUrl.replace("/discoveryqproxy", "")

    # ref. https://stackoverflow.com/a/36601467/248616
    proxiedResponse = requests.request(
        method=request.method,
        url=proxyUrl,
        headers={k: v for k, v in request.headers if k.lower() != "host"},  # exclude 'host' header
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
    )

    # Exlcude some keys in response
    # NOTE we here exclude all "hop-by-hop headers" defined by RFC 2616 section 13.5.1 ref. https://www.rfc-editor.org/rfc/rfc2616#section-13.5.1
    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]
    headers = [(k, v) for k, v in proxiedResponse.raw.headers.items() if k.lower() not in excluded_headers]

    response = Response(proxiedResponse.content, proxiedResponse.status_code, headers)
    return response


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    args = args.parse_args()

    app.run(host="0.0.0.0", debug=args.debug)

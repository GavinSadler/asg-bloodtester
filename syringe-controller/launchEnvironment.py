
import subprocess
import time

subprocess.Popen(["chromium-browser", "%U", "http://169.254.198.199/"])
time.sleep(5)
subprocess.Popen(["python", "main.py"], cwd="/home/ASG/syringe-controller")

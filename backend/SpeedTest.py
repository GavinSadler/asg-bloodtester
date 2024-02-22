
from MotorController import *
from SyringeController import Syringe

import RPi.GPIO
RPi.GPIO.setwarnings(False)

STEPS_PER_mL = 32258.06452

m = MotorController()
s = Syringe(m, STEPS_PER_mL)

lowerBoundSpeed = getStepsFromL(100 * 10**-6) / 60 # Lower bound speed (100uL/min)
upperBoundSpeed = getStepsFromL(300 * 10**-3) / 60 # Upper bound speed (300mL/min)

testDistance = int(getStepsFromL(0.2 * 10**-3)) # 0.2mL

print(f"Test distance: 0.2ml -> {testDistance} steps")

# print("Lower bound test")
# print(f"Step speed: {lowerBoundSpeed:.2f} steps/sec")
# print(f"Estimated time: {testDistance / lowerBoundSpeed:.2f} seconds")

# m.setDirection(CLOCKWISE)
# m.setStepSpeed(lowerBoundSpeed)
# m.startDelta(testDistance)

# m.getThreadBlock(60 * 3)

# m.stop()

# print("Upper bound test")
# print(f"Step speed: {upperBoundSpeed:.2f} steps/sec")
# print(f"Estimated time: {testDistance / upperBoundSpeed:.2f} seconds")

# m.setDirection(COUNTER_CLOCKWISE)
# m.setStepSpeed(upperBoundSpeed)
# m.startDelta(testDistance)



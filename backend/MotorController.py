
from threading import Event, Lock, Thread
from time import sleep

import RPi.GPIO as GPIO

# Pin definitions
PIN_ENABLE = 17
PIN_STEP = 27
PIN_DIR = 22

# Direction definition
CLOCKWISE = 0
COUNTER_CLOCKWISE = 1


class MotorController:

    def __init__(self, microstepFactor: int = 16):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(PIN_ENABLE, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(PIN_STEP, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(PIN_DIR, GPIO.OUT, initial=GPIO.LOW)

        # Depending on the hardware configuration of microsteps, this keeps track
        # of how many microsteps are in one full step. Unit is microsteps/step
        self._microstepFactor = microstepFactor

        self._delay = 0.0
        self.setRotationSpeed(1)

        self._stop = Event()
        self._stepCounterLock = Lock()
        self._motorThread: Thread = Thread()

        # Counts how many steps/microsteps this motor is at
        # Positive is clockwise, negative is counter-clockwise
        self._steps = 0  # !!! Readonly outside of the dedicated motor thread !!!

        # Keeps track of the direction of the motor
        # 0 is clockwise, 1 is counter-clockwise
        self._direction = (
            CLOCKWISE  # !!! Need to acquire _stepCounterLock to modify !!!
        )
        self.setDirection(CLOCKWISE)

    def __del__(self):
        self.stop()
        GPIO.cleanup()  # Clean up GPIO configurations

    def start(self):
        """Starts the motor for continuous motion"""
        # Stop any current operation
        self.stop()

        self._motorThread = Thread(target=self._runContinuous)
        self._motorThread.start()

    def startDelta(self, steps: int):
        """Runs the motor for the given number of steps"""
        # Stop any current operation
        self.stop()

        self._motorThread = Thread(target=self._runDelta, args=(steps,))
        self._motorThread.start()

    def startTarget(self, stepTarget: int):
        """Runs the motor until reaching the target step position"""
        # Stop any current operation
        self.stop()

        self._motorThread = Thread(target=self._runTarget, args=(stepTarget,))
        self._motorThread.start()

    def stop(self):
        """If the motor is running, this will stop the motor"""
        self._stop.set()

        # Wait for the thread to clean up, if we want to block
        if self.isRunning():
            self._motorThread.join()

        self._stop.clear()

    def isRunning(self):
        """Returns true if the motor is currently running"""
        return self._motorThread.is_alive()

    def setStepSpeed(self, stepsPerSecond: float):
        """Sets the motor's speed in steps per second."""
        # _delay, or d, is the delay between toggling the step pin on and off
        # 1 step / 2d seconds = x steps / 1 second => d = 1 / (2x)
        self._delay = 1 / (2 * stepsPerSecond)

    def setRotationSpeed(self, rotationsPerSecond: float):
        """Sets the motor's speed in rotations per second."""
        self.setStepSpeed(self.calculateSteps(rotationsPerSecond))

    def setDirection(self, newDirection: int):
        """Sets the motor's direction
        If newDirection is CLOCKWISE (0), it will move clockwise, if it is COUNTER_CLOCKWISE (1), it will move counter-clockwise.
        """

        # Lock the step counter, as it could be affected when changing directions
        self._stepCounterLock.acquire()

        if newDirection == CLOCKWISE:
            self._direction = CLOCKWISE
            GPIO.output(PIN_DIR, GPIO.LOW)
        elif newDirection == COUNTER_CLOCKWISE:
            self._direction = COUNTER_CLOCKWISE
            GPIO.output(PIN_DIR, GPIO.HIGH)

        self._stepCounterLock.release()

    def getSteps(self):
        """Returns the number of steps counted from the motor. Clockwise is positive, counter-clockwise is negative."""
        return self._steps

    def getRotations(self):
        """Returns the number of rotations from the motor. Clockwise is positive, counter-clockwise is negative."""
        return self.calculateRotations(self._steps)

    def clearSteps(self):
        """Resets the tracked number of steps"""
        self._stepCounterLock.acquire()
        self._steps = 0
        self._stepCounterLock.release()

    def calculateRotations(self, steps: int):
        """Calculates the number of rotations for a given number of steps"""
        # (1 step / 1.8 deg) * (360 deg / 1 rotation) * (n microsteps / 1 step) = 200n microsteps / 1 rotation
        # Setting this equal to x steps: x steps * 1 rotation / 200n microsteps = x / (200n) rotations
        return steps / (200 * self._microstepFactor)

    def calculateSteps(self, rotations: float):
        """Calculates the number of steps for a given number of rotations"""
        # (1 step / 1.8 deg) * (360 deg / x rotation) * (n microsteps / 1 step) = 200n microsteps / rotation
        return 200 * self._microstepFactor * rotations

    def getThreadBlock(self, timeout: float = None):
        """Will block the calling thread until the motor has finished its operation (or was stopped) with an optional timeout"""
        self._motorThread.join(timeout)

    # === Functions which are to be run as isolated motor threads ===

    def _runContinuous(self):
        """Runs the motor continuously when called, until stop flag is set"""

        # Only pull enable low when the motor is running!
        GPIO.output(PIN_ENABLE, GPIO.LOW)

        while not self._stop.isSet():

            GPIO.output(PIN_STEP, GPIO.HIGH)
            sleep(self._delay)
            GPIO.output(PIN_STEP, GPIO.LOW)
            sleep(self._delay)

            # Count the steps
            self._stepCounterLock.acquire()

            if self._direction == CLOCKWISE:
                self._steps += 1
            else:
                self._steps -= 1

            self._stepCounterLock.release()

        # Make sure to pull enable high while the motor should be 'off'
        GPIO.output(PIN_ENABLE, GPIO.HIGH)

        self._stop.clear()

    def _runDelta(self, numberOfSteps: int):
        """Run's the motor for the specified number of steps or until stop flag is set"""

        if type(numberOfSteps) != int:
            raise TypeError("numberOfSteps must be an integer")

        if numberOfSteps < 0:
            raise ValueError("numberOfSteps must be non-negative")

        # Only pull enable low when the motor is running!
        GPIO.output(PIN_ENABLE, GPIO.LOW)

        for _ in range(numberOfSteps):

            GPIO.output(PIN_STEP, GPIO.HIGH)
            sleep(self._delay)
            GPIO.output(PIN_STEP, GPIO.LOW)
            sleep(self._delay)

            # Count the steps
            self._stepCounterLock.acquire()

            if self._direction == CLOCKWISE:
                self._steps += 1
            else:
                self._steps -= 1

            self._stepCounterLock.release()

            # Since the principal mechanism in this method of moving the motor is based on total number of rotations,
            # we have to manually check to see if the user wants to stop the motor
            if self._stop.isSet():
                break

        # Make sure to pull enable high while the motor should be 'off'
        GPIO.output(PIN_ENABLE, GPIO.HIGH)

        self._stop.clear()

    def _runTarget(self, stepTarget: int):
        """Runs the motor until the specified step position is reached or until stop flag is set"""

        if type(stepTarget) != int:
            raise TypeError("stepTarget must be an integer")

        # Only pull enable low when the motor is running!
        GPIO.output(PIN_ENABLE, GPIO.LOW)

        stepDifference = abs(stepTarget - self._steps)

        while not self._stop.isSet() and stepDifference > 0:

            GPIO.output(PIN_STEP, GPIO.HIGH)
            sleep(self._delay)
            GPIO.output(PIN_STEP, GPIO.LOW)
            sleep(self._delay)

            # Count the steps
            self._stepCounterLock.acquire()

            if self._direction == CLOCKWISE:
                self._steps += 1
            else:
                self._steps -= 1

            self._stepCounterLock.release()

            stepDifference -= 1

        # Make sure to pull enable high while the motor should be 'off'
        GPIO.output(PIN_ENABLE, GPIO.HIGH)

        self._stop.clear()

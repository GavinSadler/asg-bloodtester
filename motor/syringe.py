
from motorController import *

class Syringe():
    
    def __init__(self, motor: MotorController, stepsPermL: float):
        """ Controls a syringe

        Args:
            motor (MotorController): The motor that controls the syringe assembly
            stepsPermL (float): The dispense rate of the syringe in steps of the motor per mL
        """
        
        self.motor = motor
        self._stepsPermL = stepsPermL
    
    def dispense(self, mL: float):
        """ Dispenses a given amount of mL """
        
        self.motor.setDirection = CLOCKWISE # Clockwise = dispense
        self.motor.startDelta(mL * 10**(-3) * self._stepsPermL)
    
    def retract(self, mL: float):
        """ Retracts a given amount of mL """
        
        self.motor.setDirection = COUNTER_CLOCKWISE # Counterclockwise = retract
        self.motor.startDelta(mL * 10**(-3) * self._stepsPermL)
    
    def setDispenseSpeed(self, mLperMin: float):
        """ Sets the dispense speed in mL per minute """
        # x mL / min * k steps / mL * min / 60 sec
        self.motor.setStepSpeed(mLperMin * self._stepsPermL / 60)
    
    def getStepsFrommL(self, mL: float):
        """ Returns the number of motor steps from the given amount of mL """
        return self._stepsPermL * mL
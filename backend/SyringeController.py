
from MotorController import *
import math

MICROSTEPS_PER_M = 4063894.74

class Syringe():
    
    def __init__(self, motor: MotorController, diameter_mm: float):
        """ Controls a syringe

        Args:
            motor (MotorController): The motor that controls the syringe assembly
            diameter_mm (float): The diameter of the syringe in millimeters
        """
        
        self.motor = motor
        
        # Diameter of the syringe's pump surface
        self._diameter = diameter_mm * 10**(-3)
        
        # Calculate the area of the syringe's pump surface
        self._area = (self._diameter / 2.0)**2 * math.pi
        
    
    def dispense(self, mL: float):
        """ Dispenses a given amount of mL """
        
        self.motor.setDirection(CLOCKWISE) # Clockwise = dispense
        self.motor.startDelta(self.getStepsFrommL(mL))
    
    def retract(self, mL: float):
        """ Retracts a given amount of mL """
        
        self.motor.setDirection(COUNTER_CLOCKWISE) # Counterclockwise = retract
        self.motor.startDelta(self.getStepsFrommL(mL))
    
    def dispenseContinuous(self):
        """ Dispenses continuously until stopped """
        
        self.motor.setDirection(CLOCKWISE) # Clockwise = dispense
        self.motor.start()

    def retractContinuous(self):
        """ Retracts continuously until stopped """
        
        self.motor.setDirection(COUNTER_CLOCKWISE) # Counterclockwise = retract
        self.motor.start()
    
    def setDispenseSpeed(self, uLperMin: float):
        """ Sets the dispense speed in uL per minute """
        
        LperMin = uLperMin * 10**(-6)
        LperSec = LperMin / 60
        m3perSec = LperSec * 0.001
        mperSec = m3perSec / self._area
        microstepsPerSec = mperSec * MICROSTEPS_PER_M
                
        self.motor.setStepSpeed(microstepsPerSec)
    
    def getStepsFrommL(self, mL: float):
        """ Returns the number of motor microsteps from the given amount of liquid in milliliters """
        
        l = mL * 10**(-3)
        m3 = l * 10**(-3)
        m = m3 / self._area
        microsteps = m * MICROSTEPS_PER_M
        
        return int(microsteps) 
    

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
        
        self.setDiameter(diameter_mm * 10**(-3))
        
        self.setDispenseSpeed(1)
        
    
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
        
        if self._area == 0:
            return
        
        LperMin = uLperMin * 10**(-6)
        LperSec = LperMin / 60
        m3perSec = LperSec * 0.001
        mperSec = m3perSec / self._area
        microstepsPerSec = mperSec * MICROSTEPS_PER_M
                
        self.motor.setStepSpeed(microstepsPerSec)
    
    def setCarriageSpeed(self, mmPerSecond: float):
        """ Sets the motor's speed so the syringe carriage moves at a specific speed """
        raise NotImplementedError
    
    def getStepsFrommL(self, mL: float):
        """ Returns the number of motor microsteps from the given amount of liquid in milliliters """
        
        l = mL * 10**(-3)
        m3 = l * 10**(-3)
        m = m3 / self._area
        microsteps = m * MICROSTEPS_PER_M
        
        return int(microsteps) 
    

    def setDiameter(self, newDiameter: float):
        """ Sets the diameter of the syringe for calibration purposes

        Args:
            newDiameter (float): The diameter of the syringe in meteres
        """
        self._diameter = newDiameter
        self._area = math.pi * (self._diameter / 2)**2
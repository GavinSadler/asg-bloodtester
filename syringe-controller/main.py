
from gui import Gui
from motorController import MotorController
from syringeController import Syringe
import constants

if __name__ == "__main__":
    
    motor = MotorController()
    syringe = Syringe(motor, constants.STEPS_PER_mL)
    ui = Gui(motor, syringe)
    
    del motor
    
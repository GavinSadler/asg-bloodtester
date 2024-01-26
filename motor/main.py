
from gui import Gui
from motorController import MotorController

if __name__ == "__main__":
    
    motor = MotorController()
    
    ui = Gui(motor)
    
    del motor
    
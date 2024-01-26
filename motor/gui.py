
import tkinter as tk
from motorController import MotorController
from inputField import InputField

class Gui():
        
    def __init__(self, motorController: MotorController):
        # 0 is clockwise, 1 is counter clockwise
        self.motor = motorController
        
        self.direction = 0
        self.speed = 1.0 # rotations per second
        
        self.root = tk.Tk()

        self.startStopButton = tk.Button(self.root, text="Start", command=lambda: self.startStop())
        self.startStopButton.pack()

        self.directionButton = tk.Button(self.root, text="Direction: Clockwise", command=lambda: self.changeDirection())
        self.directionButton.pack()

        self.speedScale = tk.Scale(
            self.root, from_=0.01, to=5, digits=3, resolution = 0.01, orient=tk.HORIZONTAL, command=lambda v: self.motor.setRotationSpeed(float(v))
            )
        self.speedScale.set(self.speed)
        self.speedScale.pack()
        
        self.stepsLabel = tk.Label(self.root, text="Steps: 0")
        self.stepsLabel.pack()
        
        self.rotationsLabel = tk.Label(self.root, text="Rotations: 0")
        self.rotationsLabel.pack()
        
        self.clearRotationsButton = tk.Button(self.root, text="Clear Steps", command=self.clearSteps)
        self.clearRotationsButton.pack()
        
        stepControl = InputField(self.root, "Steps:", lambda steps: self.motor.startDelta(steps), "int")
        stepControl.pack()
        
        rotationControl = InputField(self.root, "Rotations:", lambda rotations: self.motor.startDelta(int(self.motor.calculateSteps(rotations))), "float")
        rotationControl.pack()
        
        rotationControl = InputField(self.root, "mL:", lambda ml: self.motor.startDelta(int(ml*(10**5)/3.1)), "float")
        rotationControl.pack()
        
        self.updateLabels()
        
        self.root.mainloop()
    
    def changeDirection(self):
        self.direction = not self.direction
        
        label = "Direction: " + ("Clockwise" if self.direction == 0 else "Counter-clockwise")
        self.directionButton.configure(text=label)
        
        self.motor.setDirection(self.direction)
    
    def startStop(self):
        if self.motor.isRunning():
            self.motor.stop()
        else:
            self.motor.start()
        
        self.startStopButton.configure(text=("Stop" if self.motor.isRunning() else "Start"))
    
    def clearSteps(self):
        self.motor.clearSteps()
    
    def updateLabels(self):
        self.stepsLabel.configure(text=f"Steps: {self.motor.getSteps()}")
        self.rotationsLabel.configure(text=f"Rotations: {self.motor.getRotations():.2f}")
        self.startStopButton.configure(text=("Stop" if self.motor.isRunning() else "Start"))
        self.root.after(10, self.updateLabels)
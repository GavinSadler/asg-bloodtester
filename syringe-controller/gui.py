
import constants
import tkinter as tk
from motorController import MotorController
from syringeController import Syringe
from keypad import Keypad

class Gui():
        
    def __init__(self, motorController: MotorController, syringe: Syringe):
        self.motor = motorController
        self.syringe = syringe
        
        self.direction = 0
        self.speed = 1.0 # rotations per second
        
        self.root = tk.Tk()
        self.root.title("Syringe Controller")
        self.root.resizable(width=False, height=False)
        
        rootFrame = tk.Frame(self.root)
        
        # === Speed Control ===
        
        speedControl = tk.Frame()

        cWidth, cHeight = 40, 175
        canvas = tk.Canvas(speedControl, width=cWidth, height=cHeight)
        canvas.create_text(cWidth/2, cHeight/2, angle=90, text="Speed (mL/min)", font=constants.FONT)
        canvas.pack(side="left")
        
        speedScale = tk.Scale(
            speedControl, from_=0.1, to=20, digits=3, resolution = 0.1,
            orient=tk.VERTICAL, width=50, length=300, font=constants.FONT, command=lambda v: self.syringe.setDispenseSpeed(float(v))
            )
        speedScale.set(self.speed)
        speedScale.pack(side="left")
        
        speedControl.pack(pady=1)
        
        # === End of Speed Control
        
        # === Step Counter ===
        
        stepCounter = tk.Frame(rootFrame)
        
        self.stepsLabel = tk.Label(stepCounter, text="Steps: 0")
        self.stepsLabel.pack()
        
        self.rotationsLabel = tk.Label(stepCounter, text="Rotations: 0")
        self.rotationsLabel.pack()
        
        clearRotationsButton = tk.Button(stepCounter, text="Clear Steps", command=self.clearSteps)
        clearRotationsButton.pack()
        
        # Uncomment this to see the number of steps that have been taken by the stepper motor
        # stepCounter.pack(pady=1)
        
        # === End of Step Counter === 
        
        # === Dispense Control ===
        
        dispenseLabel = tk.Label(rootFrame, text="Dispense Control", font=constants.FONT)
        dispenseLabel.pack(padx=10, pady=1)
        
        keypad = Keypad(rootFrame, lambda mL: self.syringe.dispense(mL))
        keypad.pack()
        
        # === End of Dispense Control ===
        
        # === Direct Control ===
        
        controls = tk.Frame(rootFrame)

        arrowLeftImage = tk.PhotoImage(file="./arrowLeft.png")
        retractButton = tk.Button(controls, text="Dispense", image=arrowLeftImage)
        retractButton.bind("<Button-1>", lambda *_: self.syringe.retractContinuous())
        retractButton.bind("<ButtonRelease-1>", lambda *_: self.motor.stop())
        retractButton.pack(side="left", padx=1)
        
        stopImage = tk.PhotoImage(file="./stop.png")
        stopButton = tk.Button(controls, text="Stop", image=stopImage, command=self.motor.stop)
        stopButton.pack(side="left", padx=1)

        arrowRightImage = tk.PhotoImage(file="./arrowRight.png")
        dispenseButton = tk.Button(controls, text="Retract", image=arrowRightImage)
        dispenseButton.bind("<Button-1>", lambda *_: self.syringe.dispenseContinuous())
        dispenseButton.bind("<ButtonRelease-1>", lambda *_: self.motor.stop())
        dispenseButton.pack(side="left", padx=1)

        controls.pack(pady=1)
        
        # === End Of Direct Control ===
        
        rootFrame.pack(padx=3, pady=3)
        
        self.updateLabels()
        
        self.root.mainloop()
    
    def clearSteps(self):
        self.motor.clearSteps()
    
    def updateLabels(self):
        self.stepsLabel.configure(text=f"Steps: {self.motor.getSteps()}")
        self.rotationsLabel.configure(text=f"Rotations: {self.motor.getRotations():.2f}")
        self.root.after(10, self.updateLabels)

import tkinter as tk
import constants
from typing import Callable


class Keypad(tk.Frame):
    
    def __init__(self, parent: tk.Misc, callback: Callable):
        super().__init__(parent)
        
        self._callback = callback
        
        keys = [
            ['7', '8', '9'],    
            ['4', '5', '6'],    
            ['1', '2', '3'],    
            ['0', '.', 'C'],    
        ]

        entryFrame = tk.Frame(self)
        
        # place to display the number
        self.entry = tk.Entry(entryFrame, font=constants.FONT, width=6)
        self.entry.insert(0, "0.0")
        self.entry.xview_moveto(1)
        self.entry.pack(side="left")
        
        mlLabel = tk.Label(entryFrame, text="mL", font=constants.FONT)
        mlLabel.pack(side="left")
        
        startButton = tk.Button(entryFrame, text="Start", font=constants.FONT, command=lambda *_: self.submit())
        startButton.pack(side="left")
        
        entryFrame.pack()
        
        keypadFrame = tk.Frame(self)

        # create buttons using `keys`
        for y, row in enumerate(keys):
            for x, key in enumerate(row):
                # `lambda` inside `for` has to use `val=key:code(val)` 
                # instead of direct `code(key)`
                b = tk.Button(keypadFrame, text=key, font=constants.FONT, command=lambda val=key: self.input(val))
                b.grid(row=y, column=x, ipadx=10, ipady=10)
        
        keypadFrame.pack()
    
    def input(self, value):
        # C will clear the entry
        if value == 'C':
            self.entry.delete('0', tk.END)
        elif value == ".":
            # Don't allow two dots in the entry
            if self.entry.get().count(".") == 0:
                self.entry.insert(tk.END, value)
        else:
            self.entry.insert(tk.END, value)
        
    def submit(self):
        val = self.entry.get()
        error = False
        
        # Try to convert the entry into a float
        try:
            val = float(val)
        except ValueError:
            val = 0.0
            error = True

        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(val))
        
        # Only call the callback function if there was no input error
        if not error:
            self._callback(val)
                
        
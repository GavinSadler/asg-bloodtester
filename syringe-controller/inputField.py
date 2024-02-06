
import tkinter as tk
from typing import Callable

class InputField(tk.Frame):
    
    def __init__(self, parent: tk.Misc, label: str, callback: Callable[[int | float], None], valueType: str="float", buttonLabel="Go"):
        """ Generates a tk input field with some label and input field

        Args:
            parent (tk.Misc): The parent element for this label
            label (str): The label of the field
            callback (function): The callback function that will be called when the go button is pressed
            type (str): The type of value this field is looking for. 'int' or 'float' are acceptable
            buttonLabel (str): The text on the button label
        """
        super().__init__(parent)
        
        self.valueType = valueType
        self._value = 0
        self._callback = callback
        
        label = tk.Label(self, text=label, font=("Helvetica 15 bold"))
        label.pack(side="left", padx=1)
        
        self._valueEntry = tk.Entry(self, font="Helvetica 15", width=8)
        self._valueEntry.bind("<FocusOut>", lambda *_: self._validateInput())
        self._valueEntry.bind("<Return>", lambda *_: self._validateInput())
        self._valueEntry.insert(0, str(self._value)) # Puts in 0 as default
        self._valueEntry.pack(side="left", padx=1)
        
        goButton = tk.Button(self, text=buttonLabel, command=lambda *_: self._onGo(), font=("Helvetica 15 bold"))
        goButton.pack(side="left", padx=1)
        
        self._validateInput()
    
    def _validateInput(self):
        newValue = self._valueEntry.get()
        
        try:
            if self.valueType == "int":
                self._value = int(newValue)
            elif self.valueType == "float":
                self._value = float(newValue)
        except ValueError:
            pass

        self._valueEntry.delete(0, tk.END)
        self._valueEntry.insert(0, str(self._value))

    def _onGo(self):
        self._validateInput()
        self._callback(self._value)

    def getValue(self):
        """ Returns the value of this input field """
        return self._value

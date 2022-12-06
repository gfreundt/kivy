import math

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.lang import Builder


class Butt(Button):
    pass


class Calculator(BoxLayout):

    memoryValue = 0
    openAction = None
    blockDigits = False

    def digit(self, value):
        self.display = self.ids.mainDisplay.text
        if self.blockDigits:
            return

        if value == "." and "." in self.display:
            return
        if self.display == "0":
            if value == ".":
                self.display = "0."
            else:
                self.display = str(value)
        else:
            self.display += str(value)

        self.ids.mainDisplay.text = self.display

    def action(self, do):

        self.blockDigits = False
        self.display = self.ids.mainDisplay.text

        match do:
            case "^2":
                self.display = str(float(self.display) ** 2)
            case "!":
                self.display = (
                    "ERROR"
                    if "." in self.display
                    else str(math.factorial(int(self.display)))
                )
                self.blockDigits = True
            case "1/":
                self.display = str(float(self.display) ** -1)
            case "sq_root":
                self.display = str(math.sqrt(float(self.display)))
            case "abs":
                self.display = str(abs(float(self.display)))
            case "logy":
                self.display = "0"
                self.openAction = "ln"
            case "e":
                self.display = str(math.e)
            case "pi":
                self.display = str(math.pi)
            case "log10":
                self.display = str(math.log10(float(self.display)))
            case "+/-":
                self.display = str(-(float(self.display)))
            case "ln":
                self.display = str(math.log(float(self.display)))
            case "cos":
                # TODO: check for DEG or RAD
                self.display = str(math.cos(float(self.display)))
            case "sin":
                self.display = str(math.sin(float(self.display)))
            case "tan":
                self.display = str(math.tan(float(self.display)))
            case "rooty":
                self.display = "0"
                self.openAction = "** -"
            case "mod":
                self.display = "0"
                self.openAction = "remainder"
            case "e^x":
                self.display = str(math.e ** (float(self.display)))
            case "M+":
                self.memoryValue += int(self.display)
            case "M-":
                self.memoryValue -= int(self.display)
            case "MR":
                self.display = str(self.memoryValue)
            case "MC":
                self.memoryValue = 0
            case "clear_all":
                self.display = "0"
                self.openAction = None
            case "back_one":
                if len(self.display) == 1:
                    self.display = "0"
                else:
                    self.display = self.display[:-1]
            case "+" | "-" | "*" | "/" | "**":
                # TODO: chained operations should yield results
                self.openAction = do
                self.openActionValue = self.display
                self.display = "0"
            case "=":
                if self.openAction:
                    self.display = str(
                        eval(f"{self.openActionValue} {self.openAction} {self.display}")
                    )
                    self.openAction = None

        # post processing: delete "." and everything after if only 0s in decimal
        reverse = self.display[::-1]
        while "." in reverse and reverse[0] == "0":
            reverse = reverse[1:]
        if reverse[0] == ".":
            reverse = reverse[1:]
        self.display = reverse[::-1]

        self.ids.mainDisplay.text = self.display
        self.ids.memLabel.text = " " if self.memoryValue == 0 else "M"

    def switch(self, lever):
        match lever:
            case "angles":
                self.ids.angleUnitSwitch.text = (
                    "DEG" if self.ids.angleUnitSwitch.text == "RAD" else "RAD"
                )


class CalculatorApp(App):
    Window.size = (350, 600)
    Window.clearcolor = (0.102, 0.0, 0.102, 1)

    def build(self):
        return Calculator()


# Builder.load_file("calculator.kv")
CalculatorApp().run()

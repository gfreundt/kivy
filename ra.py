import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.lang import Builder


kivy.require("2.1.0")
Builder.load_file("rA.kv")


class rALayout(BoxLayout):
    pass


class mainApp(App):
    def build(self):
        return rALayout()


mainApp().run()

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder

Window.size = (640,480)

global screen

screen = ScreenManager()

class SplashScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class RTKActivationScreen(Screen):
    pass

class RTKSetupScreen(Screen):
    pass

screen.add_widget(SplashScreen(name='splash'))
screen.add_widget(MainScreen(name='main'))



class RowRTK(MDApp):
    def build(self):
        kv = Builder.load_file("model1.kv")
        screen = kv
        return screen
    
if __name__ == "__main__":
    RowRTK().run()
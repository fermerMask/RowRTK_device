from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from RTKKib import rtklib

Window.size = (640,480)

nmea = rtklib.NMEA
logger = rtklib.Logger
global screen

screen = ScreenManager()

class SplashScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class StandaloneScreen(Screen):
    def back_screen(self):
        self.manager.current = self.manager.previous()

class RTKActivationScreen(Screen):
    def back_screen(self):
        self.manager.current = self.manager.previous()

class RTKSetupScreen(Screen):
    def back_screen(self):
        self.manager.current = self.manager.previous()

screen.add_widget(SplashScreen(name='splash'))
screen.add_widget(MainScreen(name='main'))
screen.add_widget(RTKSetupScreen(name='setting'))
screen.add_widget(StandaloneScreen(name='standalone'))
screen.add_widget(RTKActivationScreen(name='rtkactivation'))



class RowRTK(MDApp):
    def build(self):
        kv = Builder.load_file("model1.kv")
        screen = kv
        return screen
    
if __name__ == "__main__":
    RowRTK().run()
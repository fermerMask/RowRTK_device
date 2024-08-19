from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.filemanager import MDFileManager
from RTKKib import rtklib
import os
import json
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
    def start(self):
        rtklib.start()

class RTKActivationScreen(Screen):
   pass

class RTKSetupScreen(Screen):
    config_file = 'config.json'

    def open_file_manager(self):
        self.file_manager.show(os.path.expanduser("~"))
    
    def select_path(self,path):
        self.ids.log_file.text = path
        self.save_config()
        self.exit_manger()
    
    def exit_manager(self,*args):
        self.file_manager.close()
    
    def on_pre_enter(self):
        self.load_config()
    
    def save_config(self):
        config_data = {
            'base_station':self.ids.base_station.text,
            'log_file': self.ids.log_file.text
        }
        with open(self.config_file,'w') as f:
            json.dump(config_data,f)
    
    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file,'r') as f:
                config_data = json.load(f)
            self.ids.base_station.text = config_data.get('base_station','')
            self.ids.log_file.text = config_data.get('log_file','')
    
    def on_base_station_changed(self):
        self.save_config()


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
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.filemanager import MDFileManager
from tkinter import filedialog
from kivy.uix.popup import Popup
from RTKKib.rtklib2 import NMEA,RTKController
from RTKKib.configmanager import ConfigManager
from kivy.properties import StringProperty
import os
import json
from datetime import datetime
Window.size = (640,480)

global screen 

screen = ScreenManager()

class SplashScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class StandaloneScreen(Screen):
    config_file = 'config.json'
    
    velocity = StringProperty("0.00")
    time = StringProperty("0:00.0")
    longitude = StringProperty("000.0000")
    latitude = StringProperty("00.0000")
    mode = StringProperty("N/A")
    
    def start_stop_toggle(self):
        if self.ids.start_stop_button.icon == "play":
            self.ids.start_stop_button.icon = "pause"
            self.ids.start_stop_button.text = "Pause"
            #self.ids.stop_button.disable = False
            self.start()
        else:
            self.ids.start_stop_button.icon = "play"
            self.ids.start_stop_button.text = "Start"
            self.stop()

    def start(self):
        config_manager = ConfigManager(self.config_file)
        
        folder = config_manager.get_value('log_file')
        rover_from = config_manager.get_value('rover_from')
        
        self.rtk_controller = RTKController(update_callback=self.update_display)
        self.rtk_controller.start(folder,rover_from)

        if self.rtk_controller.update_callback:
            print("Call back is set.")
        else:
            print("Call back is not set")

    def stop(self):
        self.rtk_controller.stop()
        print("stop")

    def update_display(self,data):
        self.time = f"{float(data['time']):.3f}"       # 時間を小数第3位まで表示
        self.latitude = f"{float(data['latitude']):.3f}"  # 緯度を小数第3位まで表示
        self.longitude = f"{float(data['longitude']):.3f}" # 経度を小数第3位まで表示
        self.velocity = f"{float(data['velocity']):.3f}"   # 速度を小数第3位まで表示
        self.alt = f"{float(data['alt']):.3f}"           # 高度を小数第3位まで表示
        self.mode = str(data['mode'])

class RTKActivationScreen(Screen):
    config_file = 'config.json'

    def connect_toggle(self):
        if self.ids.connect_button.icon == "lan-connect":
            self.ids.connect_button.icon = "lan-disconnect"
            self.ids.connect_button.text = "Pause"
            #self.ids.stop_button.disable = False
            self.start()
        else:
            self.ids.connect_button.icon = "lan-connect"
            self.ids.connect_button.text = "Start"
            self.stop()

    def start(self):
        config_manager = ConfigManager(self.config_file)
        base_station = config_manager.get_value('base_station')
        folder = config_manager.get_value('log_file')
        #controller.start()
        print(base_station)

    def stop(self):
        print("stop")

class RTKSetupScreen(Screen):

    config_file = "config.json"  # 設定ファイルのパスを指定

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.select_path(str(directory))
            
    def select_path(self, path):
        self.ids.log_file.text = path
        self.save_config()
    
    def on_pre_enter(self):
        self.load_config()
    
    def save_config(self):
        config_manager = ConfigManager(self.config_file)
        config_data = config_manager.get_config()

        # 現在の設定を更新
        config_data['base_station'] = self.ids.base_station.text
        config_data['log_file'] = self.ids.log_file.text + '/'
        config_data['rover_to'] = self.ids.rover_to.text
        config_data['rover_from'] = self.ids.rover_from.text

        with open(self.config_file, 'w') as f:
            json.dump(config_data, f)
    
    def load_config(self):
        config_manager = ConfigManager(self.config_file)
        config_data = config_manager.get_config()

        # UIに設定を反映
        self.ids.base_station.text = config_data.get('base_station', '')
        self.ids.log_file.text = config_data.get('log_file', '')
        self.ids.rover_to.text = config_data.get('rover_to', '')
        self.ids.rover_from.text = config_data.get('rover_from', '')
    
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

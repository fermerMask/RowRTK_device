from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.lang import Builder
import subprocess
import threading
import time
from kivy.app import App

Builder.load_file('test.kv')

class RTKController(BoxLayout):
    # Properties to bind to the KV language
    lat = StringProperty("")
    lon = StringProperty("")
    mode = StringProperty("")
    vel = StringProperty("")
    alt = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.p_base = None
        self.p_rtk = None
        self.kill_update = False
        self.th_logger = None
        self.th_updater = None
    
    def connect_base(self):
        base = self.ids.base_input.text
        rover_to = self.ids.rover_to_input.text
        cmd = f'exec {self.str2str} -in ntrip://{base} -out serial://{rover_to}'
        self.p_base = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.ids.disconnect_button.disabled = False
        self.ids.connect_button.disabled = True
    
    def disconnect_base(self):
        if self.p_base:
            self.p_base.kill()
        self.ids.disconnect_button.disabled = True
        self.ids.connect_button.disabled = False
    
    def start(self):
        logfile = self.ids.logfile_input.text
        rover_from = self.ids.rover_from_input.text
        port, bps = rover_from.split(':')
        cmd = f'exec cu -s {bps} -l /dev/{port}'
        self.p_rtk = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.th_logger = threading.Thread(target=self.log_gnss, args=(logfile,))
        self.th_logger.start()
        self.th_updater = threading.Thread(target=self.update_status, daemon=True)
        self.th_updater.start()
        self.ids.start_button.disabled = True
        self.ids.stop_button.disabled = False
    
    def log_gnss(self, logfile):
        # Implement GNSS logging logic here
        pass
    
    def update_status(self):
        while not self.kill_update:
            # Dummy values for demonstration
            self.lat = f'{37.7749:.8f}'
            self.lon = f'{-122.4194:.8f}'
            self.mode = 'RTK Fix'
            self.vel = f'{1.234:.3f}'
            self.alt = f'{100.123:.3f}'
            time.sleep(0.5)
    
    def stop(self):
        self.kill_update = True
        if self.p_rtk:
            self.p_rtk.stdin.write('~.')
            time.sleep(1)
            self.p_rtk.kill()
        self.ids.start_button.disabled = False
        self.ids.stop_button.disabled = True


class MyApp(App):
    def build(self):
        return RTKController()

if __name__ == '__main__':
    MyApp().run()
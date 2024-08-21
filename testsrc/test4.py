from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, StringProperty
from kivy.clock import Clock
from kivymd.app import MDApp

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: dp(20)

    MDLabel:
        id: timer_label
        text: app.time_display
        halign: 'center'
        font_style: 'H2'

    BoxLayout:
        size_hint_y: None
        height: self.minimum_height
        spacing: dp(20)

        MDRaisedButton:
            text: 'Start'
            on_press: app.start_timer()
            disabled: app.is_running

        MDRaisedButton:
            text: 'Stop'
            on_press: app.stop_timer()
            disabled: not app.is_running

        MDRaisedButton:
            text: 'Reset'
            on_press: app.reset_timer()
            disabled: app.is_running
'''

class TimerApp(MDApp):
    time_display = StringProperty("00:00:00")
    is_running = BooleanProperty(False)

    def build(self):
        return Builder.load_string(KV)

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = 0
            self.event = Clock.schedule_interval(self.update_time, 1)

    def stop_timer(self):
        if self.is_running:
            self.is_running = False
            self.event.cancel()

    def reset_timer(self):
        self.time_display = "00:00:00"
        self.start_time = 0

    def update_time(self, dt):
        self.start_time += 1
        minutes, seconds = divmod(self.start_time, 60)
        hours, minutes = divmod(minutes, 60)
        self.time_display = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

if __name__ == '__main__':
    TimerApp().run()

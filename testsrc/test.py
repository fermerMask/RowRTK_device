from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App

KV = '''
ScreenManager:
    MainScreen:

<MainScreen>:
    name: 'main'

    BoxLayout:
        orientation: 'vertical'
        
        # トップバー（時間、アイコン）
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            padding: [10, 0]
            spacing: 10

            Label:
                text: "10:06"
                color: 0, 0, 0, 1
                font_size: '20sp'

            Label:
                text: "Icon"
                font_size: '20sp'
        
        # 地図表示エリア
        Label:
            text: "map"
            size_hint_y: 0.5
            canvas.before:
                Color:
                    rgba: 0.9, 0.9, 0.9, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

        # 通知バナー
        Label:
            text: "heart rate sensor was disconnected"
            size_hint_y: None
            height: '40dp'
            color: 1, 1, 1, 1
            canvas.before:
                Color:
                    rgba: 1, 0.6, 0, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
        
        # データ表示エリア
        GridLayout:
            cols: 2
            size_hint_y: None
            height: '150dp'
            padding: [10, 10]
            spacing: 10

            Label:
                text: "heartbeat (bpm)"
            Label:
                text: "-"
            Label:
                text: "velocity (km/h)"
            Label:
                text: "-"
            Label:
                text: "time"
            Label:
                text: "00:00:01"
            Label:
                text: "distance (km)"
            Label:
                text: "0.00"
        
        # ページインジケータ
        BoxLayout:
            size_hint_y: None
            height: '30dp'
            Label:
                text: "● ○ ○"
                font_size: '20sp'
        
        # 操作ボタン
        BoxLayout:
            size_hint_y: None
            height: '60dp'
            padding: [10, 10]
            Button:
                text: "stop"
                size_hint: None, None
                size: '150dp', '40dp'
                background_normal: ''
                background_color: 1, 0, 0, 1
                color: 1, 1, 1, 1
'''

class MainScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        return Builder.load_string(KV)

MyApp().run()

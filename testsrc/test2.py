from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np

KV = '''
ScreenManager:
    StandaloneScreen:

<StandaloneScreen>:
    name: 'standalone'
    MDBoxLayout:
        orientation: "vertical"

        MDToolbar:
            title: "GPS Stand Alone"
            left_action_items: [["arrow-left", lambda x: setattr(root.manager, 'current', 'main')]]
            md_bg_color: 188/255, 227/255, 217/255, 1
            elevation: 10

        # グラフ表示エリア
        BoxLayout:
            id: graph_area
            size_hint_y: 0.5  # グラフの高さを調整
            padding: [10, 20]
            height: dp(230)
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [20]

        MDGridLayout:
            cols: 2
            size_hint_y: None
            height: dp(130)
            padding: [10, 10]
            spacing: 10

            MDLabel:
                text: "Time"

            MDLabel:
                id: time
                text: "0:00:0"
                font_style: "H6"

            MDLabel:
                text: "Velocity (m/s)"
            
            MDLabel:
                id: velocity
                text: "0.00"
                font_style: "H6"
            
            MDLabel:
                text: "Distance (km)"
            
            MDLabel:
                id: distance
                text: "0.00"
                font_style: "H6"
        
        # Start and Stop Buttons
        MDFillRoundFlatIconButton:
            id: start_stop_button
            icon: "play"
            text: "Start"
            pos_hint: {"center_x": 0.5}
            on_release:
                root.start_stop_toggle()
'''

class StandaloneScreen(Screen):
    def on_enter(self):
        # デモ用データを作成してグラフを表示
        self.update_graph()

    def update_graph(self):
        # グラフを生成
        t = np.linspace(0, 10, 100)
        y = np.sin(t)

        fig, ax = plt.subplots()
        ax.plot(t, y)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Velocity (m/s)")
        ax.set_title("Velocity over Time")

        # KivyのキャンバスにMatplotlibのグラフを追加
        graph = FigureCanvasKivyAgg(fig)
        self.ids.graph_area.clear_widgets()
        self.ids.graph_area.add_widget(graph)

class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    MainApp().run()


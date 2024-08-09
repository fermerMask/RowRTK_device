from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from datetime import datetime

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: 10  # 全体にパディングを追加
    spacing: 10  # セクション間のスペースを設定

    # 上部の画面 (時計)
    BoxLayout:
        size_hint_y: 0.5
        padding: [10, 20]  # 上下にパディングを追加

        canvas.before:
            Color:
                rgba: 0.9, 0.9, 0.9, 1  # 背景色を指定
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [20]  # 角を丸くする

        MDLabel:
            id: time_label
            text: "00:00:00"
            halign: "center"
            theme_text_color: "Primary"
            font_style: "H2"

    # 下部の画面 (2分割)
    BoxLayout:
        size_hint_y: 0.5
        spacing: 10  # 左右のセクション間のスペースを設定

        # 左側の画面 (日付)
        BoxLayout:
            padding: [10, 20]  # 上下にパディングを追加

            canvas.before:
                Color:
                    rgba: 0.9, 0.9, 0.9, 1  # 背景色を指定
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [20]  # 角を丸くする

            MDLabel:
                id: date_label
                text: "YYYY-MM-DD"
                halign: "center"
                theme_text_color: "Primary"
                font_style: "H4"

        # 右側の画面 (適当なデータ)
        BoxLayout:
            padding: [10, 20]  # 上下にパディングを追加

            canvas.before:
                Color:
                    rgba: 0.9, 0.9, 0.9, 1  # 背景色を指定
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [20]  # 角を丸くする

            MDLabel:
                text: "Sample Data"
                halign: "center"
                theme_text_color: "Primary"
                font_style: "H4"
'''

class SplitScreenApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_interval(self.update_time, 1)

    def update_time(self, *args):
        now = datetime.now()
        self.root.ids.time_label.text = now.strftime('%H:%M:%S')
        self.root.ids.date_label.text = now.strftime('%Y-%m-%d')

if __name__ == '__main__':
    SplitScreenApp().run()

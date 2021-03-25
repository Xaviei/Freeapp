#main.py
import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.label import CoreLabel

def collides(rect1,rect2):
    r1x = rect1[0][0]
    r1y = rect1[0][1]
    r2x = rect2[0][0]
    r2y = rect2[0][1]
    r1w = rect1[1][0]
    r1h = rect1[1][1]
    r2w = rect2[1][0]
    r2h = rect2[1][1]

    if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
        return True
    else:
        return False

class GameWidget(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed,self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self._score_label = CoreLabel(text='Score: 0')
        self._score_label.refresh()


        with self.canvas:
            self.player = Rectangle(source='images\Skeleguy01 (1).png', pos=(0,0), size=(100,100))
            self._score_instructions = Rectangle(texture=self._score_label.texture, pos=(700,0),size=self._score_label.texture.size)


        self.keysPressed = set()

        Clock.schedule_interval(self.move_step,0)

        self.sound = SoundLoader.load('placeholder')

        print(self.size)
    
    @property
    def score(self):
        return self._score_label

    @score.setter
    def score(self,value):
        self._score = value
        self._score_label.text = "Score: " + str(value)
        self._score_instructions.texture = self._score_label.texture
        self._score_instructions.size = self._score_label.texture.size

            


    
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self,keyboard,keycode,text,modifiers):
        self.keysPressed.add(text)

    def _on_key_up(self,keyboard,keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)

    def move_step(self,dt):
        currentx = self.player.pos[0]
        currenty = self.player.pos[1]

        step_size = 200 * dt

        if 'w' in self.keysPressed:
            currenty += step_size
        
        if 's' in self.keysPressed:
            currenty -= step_size
        
        if 'a' in self.keysPressed:
            currentx -= step_size

        if 'd' in self.keysPressed:
            currentx += step_size

        self.player.pos = (currentx, currenty)
        


class MyApp(App):
    def build(self):
        return GameWidget()

if __name__ == "__main__":
    app = MyApp()
    app.run()



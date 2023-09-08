from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from src.ui.drawing_widget import DrawingWidget
from src.ui.main_screen_widget import MainScreen


class DqlApp(App):
  def build(self) -> MainScreen:
    self.main_screen = MainScreen()
    
    self.painter = DrawingWidget()
    self.main_screen.add_widget(self.painter)
    
    clear_btn = Button(text='Clear')
    clear_btn.bind(on_release=self.clear_canvas)
    self.main_screen.add_widget(clear_btn)    

    Clock.schedule_interval(self.main_screen.update, 1.0/60.0)
    
    return self.main_screen

  def clear_canvas(self, obj): # clear button
        self.painter.canvas.clear()
        self.main_screen.clear_sand_density()


if __name__ == '__main__':
  DqlApp().run()
from kivy.app import App
from kivy.clock import Clock
from src.ui.drawing_widget import DrawingWidget
from src.ui.main_screen_widget import MainScreen


class DqlApp(App):
  def build(self) -> MainScreen:
    main_screen = MainScreen()
    self.painter = DrawingWidget()
    main_screen.add_widget(self.painter)

    Clock.schedule_interval(main_screen.update, 1.0/60.0)
    
    return main_screen


if __name__ == '__main__':
  DqlApp().run()
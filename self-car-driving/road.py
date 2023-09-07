from constants import CAR_NORMAL_VELOCITY
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock

class Car(Widget):
  angle = NumericProperty(0)
  rotation = NumericProperty(0)


class LeftSensor(Widget):
  pass


class FrontSensor(Widget):
  pass


class RightSensor(Widget):
  pass


class MainScreen(Widget):
  car = ObjectProperty(None)
  left_sensor = ObjectProperty(None)
  front_sensor = ObjectProperty(None)
  right_sensor = ObjectProperty(None)

  def set_car_center_and_velocity(self):
    self.car.center = self.center
    self.car.velocity = CAR_NORMAL_VELOCITY

  def update(self, dt):
    pass


class DqlApp(App):
  def build(self) -> MainScreen:
    main_screen = MainScreen()

    main_screen.set_car_center_and_velocity()

    Clock.schedule_interval(main_screen.update, 1.0/60.0)

    return main_screen


if __name__ == '__main__':
  DqlApp().run()
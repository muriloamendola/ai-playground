from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.graphics import Color


class DrawingWidget(Widget):
  def __init__(self, **kwargs):
    super(DrawingWidget, self).__init__(**kwargs)
    self.line = None
    self.color = (1, 1, 1, 1)  # Default color (white)

    self.last_x = 0
    self.last_y = 0

  def _update_sand_density(self, x:int, y:int, line: bool=False) -> None:
    self.last_x = int(x)
    self.last_y = int(y)

    self.parent.set_sand_density(x=x, y=y, line=line)

  def on_touch_down(self, touch):
    with self.canvas:
      Color(*self.color)
      self.line = Line(points=(touch.x, touch.y), width=10)
      self._update_sand_density(x=touch.x, y=touch.y)
          

  def on_touch_move(self, touch):
    if self.line:
      self.line.points += (touch.x, touch.y)
      self._update_sand_density(x=touch.x, y=touch.y, line=True)
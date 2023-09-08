from src.constants import Position
from kivy.vector import Vector


class Sensor():
  position: Position
  signal: float

  def __init__(self) -> None:
    self.position = Position(x=0, y=0)
    self.signal = 0

  def get_pos(self) -> Vector:
    return Vector([self.position.x, self.position.y])

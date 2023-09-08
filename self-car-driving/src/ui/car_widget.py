import numpy as np

from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from src.ui.sensor import Sensor

from src.constants import Position
from src.constants import SENSOR_WIDTH
from src.constants import CAR_ROTATION_BASE
from src.constants import DISTANCE_BETWEEN_CAR_SENSOR


class CarWidget(Widget):
  angle = NumericProperty(0)
  rotation = NumericProperty(0)
  velocity: Position = Position(x=0, y=0)
  left_sensor = Sensor()
  front_sensor = Sensor()
  right_sensor = Sensor()

  def _update_car_position(self) -> None:
    """
    Updating the position of the car according to its last position and velocity
    """
    self.pos = Vector(*[self.velocity.x, self.velocity.y]) + self.pos

  def _update_sensors_position(self) -> None:
    front_sensor_pos: Vector = CAR_ROTATION_BASE.rotate(self.angle) + self.pos
    self.front_sensor.position = Position(x=front_sensor_pos[0], y=front_sensor_pos[1])
    
    left_sensor_position = CAR_ROTATION_BASE.rotate((self.angle+DISTANCE_BETWEEN_CAR_SENSOR)%360) + self.pos
    self.left_sensor.position = Position(x=left_sensor_position[0], y=left_sensor_position[1])

    right_sensor_position = CAR_ROTATION_BASE.rotate((self.angle-DISTANCE_BETWEEN_CAR_SENSOR)%360) + self.pos
    self.right_sensor.position = Position(x=right_sensor_position[0], y=right_sensor_position[1])

  def _update_sensors_signal(self, sand) -> None:
    """
    Sensors are installed into the car to check the density of sand around the car. 
    This density is the signal for the sensor.

    sand is an array that has as many cells as our graphic interface has pixels. 
    Each cell has a one if there is sand, 0 otherwise.
    """
    def get_signal(x: int, y: int) -> int:
      """
      Sum the density around the sensor. 
      We get all the cells around the sensor (Matrix 20x20), sum the values and divide by 400 (number of matrix cells).
      """
      QTY_POINTS_TO_GET_AROUND = 10
      x = int(x)
      y = int(y)
      sum_of_density_in_cells = np.sum(sand[x-QTY_POINTS_TO_GET_AROUND:x+QTY_POINTS_TO_GET_AROUND, y-QTY_POINTS_TO_GET_AROUND:y+QTY_POINTS_TO_GET_AROUND])
      density = sum_of_density_in_cells / 400

      # checking if sensor is out of the map (using sand to get the map size)
      sand_shape = sand.shape # tuple like (width,height) => (1600,1200)
      sand_longueur = sand_shape[0]
      sand_largeur = sand_shape[1]

      if x > sand_longueur - SENSOR_WIDTH or x < SENSOR_WIDTH or \
         y > sand_largeur - SENSOR_WIDTH or y < SENSOR_WIDTH:
        density = 1 # sand detected

      return density
    
    self.front_sensor.signal = get_signal(x=self.front_sensor.position.x, y=self.front_sensor.position.y)
    self.left_sensor.signal = get_signal(x=self.left_sensor.position.x, y=self.left_sensor.position.y)
    self.right_sensor.signal = get_signal(x=self.right_sensor.position.x, y=self.right_sensor.position.y)

  def move(self, rotation: int, sand):
    self._update_car_position()
    self.rotation = rotation
    self.angle = self.angle + self.rotation

    self._update_sensors_position()
    self._update_sensors_signal(sand)

import numpy as np
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.clock import Clock
from kivy.vector import Vector
from collections import namedtuple

from ai import Dqn

from constants import INPUT_SIZE
from constants import LIVING_PENALTY
from constants import Actions
from constants import ACTIONS_ROTATION
from constants import DISTANCE_BETWEEN_CAR_SENSOR
from constants import CAR_WIDTH
from constants import SENSOR_WIDTH
from constants import CAR_ROTATION_BASE
from constants import CAR_NORMAL_VELOCITY
from constants import CAR_LOW_VELOCITY
from constants import WORST_REWARD
from constants import BAD_REWARD
from constants import GOOD_REWARD


Position = namedtuple('Position', ['x', 'y'])

class Sensor():
  position: Position
  signal: float

  def __init__(self) -> None:
    self.position = Position(x=0, y=0)
    self.signal = 0

  def get_pos(self) -> Vector:
    return Vector([self.position.x, self.position.y])

class Car(Widget):
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


class LeftSensor(Widget):
  pass


class FrontSensor(Widget):
  pass


class RightSensor(Widget):
  pass


class MainScreen(Widget):
  last_position: Position = Position(x=0, y=0)
  last_reward: int = 0
  last_distance: float = 0
  longueur: int = 0
  largeur: int = 0
  goal: Position # destination point
  sand = []
  cars_driver = Dqn(input_size=INPUT_SIZE, nb_action=len(Actions), gamma=LIVING_PENALTY)
  
  def on_size(self, instance, value):
    """
    This method is called everytime the screen is resized
    """
    self.longueur = self.width
    self.largeur = self.height
    self.sand = np.zeros((self.longueur,self.largeur)) # initializing the sand array with only zeros    
    self.goal = Position(x=CAR_WIDTH, y=self.largeur - CAR_WIDTH)

  def set_car_center_and_velocity(self):
    self.car.center = self.center
    self.car.velocity = CAR_NORMAL_VELOCITY

  def _get_cars_orientation(self) -> float:
    """
    Direction of the car with respect to the goal (if the car is heading perfectly towards the goal, then orientation = 0)
    """
    # difference of x and y coordinates between the goal and the car
    x_between_goal_car = self.goal.x - self.car.x
    y_between_goal_car = self.goal.y - self.car.y
    distance_goal_car = (x_between_goal_car, y_between_goal_car)

    return Vector(*self.car.velocity).angle(distance_goal_car) / 180
  
  def _get_distance_between_car_and_goal(self) -> float:
    """
    Form: distance = sqrt((x2 - x1)^2 + (y2 - y1)^2)
    """
    return np.sqrt((self.car.x - self.goal.x)**2 + (self.car.y - self.goal.y)**2)

  def _checks_goal_reached(self, distance: float) -> None:
    """
    When the car reaches its goal, it needs to return to the origin
    """
    if distance < 100: 
      new_x = self.width - self.goal.x
      new_y = self.height - self.goal.y
      self.goal = Position(x=new_x, y=new_y)

  def _is_the_car_on_sand(self) -> bool:
    """
    Checks if the cell where the car is, has density greather than 0
    """
    return self.sand[int(self.car.x),int(self.car.y)] > 0
  
  def _is_the_car_on_screen_edge(self) -> bool:
    """
    This methods checks if the car is on screen edges
    """
    on_edge = False  

    if self.car.x < 10: # if the car is in the left edge of the frame
      self.car.x = 10
      on_edge = True
    elif self.car.x > self.width-10: # if the car is in the right edge of the frame
      self.car.x = self.width-10
      on_edge = True
    elif self.car.y < 10: # if the car is in the bottom edge of the frame
      self.car.y = 10
      on_edge = True
    elif self.car.y > self.height-10: # if the car is in the upper edge of the frame
      self.car.y = self.height-10
      on_edge = True

    return on_edge
      
  def update(self, dt):    
    orientation = self._get_cars_orientation()
        
    last_signal = [self.car.front_sensor.signal, self.car.left_sensor.signal, self.car.right_sensor.signal, orientation, -orientation]
    action = self.cars_driver.update(self.last_reward, last_signal)
    rotation = ACTIONS_ROTATION[int(action.item())] 
    self.car.move(rotation, self.sand)

    distance = self._get_distance_between_car_and_goal()
    self._checks_goal_reached(distance)

    # Dealing with rewards
    if self._is_the_car_on_sand():
      self.car.velocity = CAR_LOW_VELOCITY.rotate(self.car.angle)
      self.last_reward = WORST_REWARD 
    else:
      self.car.velocity = CAR_NORMAL_VELOCITY.rotate(self.car.angle)
      self.last_reward = BAD_REWARD + (GOOD_REWARD if distance < self.last_distance else 0)

    if self._is_the_car_on_screen_edge():
      self.last_reward = WORST_REWARD

    # update screen elements 
    self.front_sensor.pos = self.car.front_sensor.get_pos()
    self.left_sensor.pos = self.car.left_sensor.get_pos()
    self.right_sensor.pos = self.car.right_sensor.get_pos()

    # Updating the last distance from the car to the goal
    self.last_distance = distance


class DqlApp(App):
  def build(self) -> MainScreen:
    main_screen = MainScreen()

    main_screen.set_car_center_and_velocity()

    Clock.schedule_interval(main_screen.update, 1.0/60.0)

    return main_screen


if __name__ == '__main__':
  DqlApp().run()
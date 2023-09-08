import numpy as np
from kivy.uix.widget import Widget
from kivy.vector import Vector
from src.ui.car_widget import CarWidget
from src.ui.sensor_widget import SensorWidget

from src.ai.dqn import Dqn

from src.constants import Position
from src.constants import INPUT_SIZE
from src.constants import LIVING_PENALTY
from src.constants import Actions
from src.constants import ACTIONS_ROTATION
from src.constants import CAR_WIDTH
from src.constants import CAR_NORMAL_VELOCITY
from src.constants import CAR_LOW_VELOCITY
from src.constants import WORST_REWARD
from src.constants import BAD_REWARD
from src.constants import GOOD_REWARD
from src.constants import DISTANCE_TO_REACH_GOAL
from src.constants import EDGE_SIZE
from src.constants import SENSOR_WIDTH


class MainScreen(Widget):
  last_position: Position = Position(x=0, y=0)
  last_reward: int = 0
  last_distance: float = 0
  longueur: int = 0
  largeur: int = 0
  goal: Position # destination point
  sand = []
  cars_driver = Dqn(input_size=INPUT_SIZE, output_size=len(Actions), gamma=LIVING_PENALTY)
  
  car: CarWidget
  front_sensor: SensorWidget
  left_sensor: SensorWidget
  right_sensor: SensorWidget

  def on_size(self, instance, value):
    """
    This method is called everytime the screen is resized
    """
    self.longueur = self.width
    self.largeur = self.height
    self.sand = np.zeros((self.longueur,self.largeur)) # initializing the sand array with only zeros    
    self.goal = Position(x=CAR_WIDTH, y=self.largeur - CAR_WIDTH)

    self.car = self.ids.car
    self.front_sensor = self.ids.front_sensor
    self.left_sensor = self.ids.left_sensor
    self.right_sensor = self.ids.right_sensor

    self._set_car_center_and_velocity()
    
  def _set_car_center_and_velocity(self):
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
    if distance < DISTANCE_TO_REACH_GOAL: 
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

    if self.car.x < EDGE_SIZE: # if the car is in the left edge of the frame
      self.car.x = EDGE_SIZE
      on_edge = True
    elif self.car.x > self.width-EDGE_SIZE: # if the car is in the right edge of the frame
      self.car.x = self.width-EDGE_SIZE
      on_edge = True
    elif self.car.y < EDGE_SIZE: # if the car is in the bottom edge of the frame
      self.car.y = EDGE_SIZE
      on_edge = True
    elif self.car.y > self.height-EDGE_SIZE: # if the car is in the upper edge of the frame
      self.car.y = self.height-EDGE_SIZE
      on_edge = True

    return on_edge
  
  def set_sand_density(self, x:int, y:int, line: bool = False) -> None:
    x = int(x)
    y = int(y)
    
    if line:
      self.sand[x-SENSOR_WIDTH:x+SENSOR_WIDTH, y-SENSOR_WIDTH:y+SENSOR_WIDTH] = 1
    else:
      self.sand[x, y] = 1
      
  def update(self, dt):    
    orientation = self._get_cars_orientation()
        
    last_signal = [self.car.front_sensor.signal, self.car.left_sensor.signal, self.car.right_sensor.signal, orientation, -orientation]
    action = self.cars_driver.update(self.last_reward, last_signal)
    rotation = ACTIONS_ROTATION[action] 
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

from enum import Enum
from kivy.vector import Vector

# Car constants
CAR_NORMAL_VELOCITY = Vector(6,0)
CAR_LOW_VELOCITY = Vector(1,0)
CAR_WIDTH = 20
SENSOR_WIDTH = 10
DISTANCE_BETWEEN_CAR_SENSOR = CAR_WIDTH + SENSOR_WIDTH
CAR_ROTATION_BASE = Vector(DISTANCE_BETWEEN_CAR_SENSOR, 0)

# GAME constants
class Actions(Enum):
  FRONT = 0
  LEFT = 1
  RIGHT = 2

ACTIONS_ROTATION = [0, CAR_WIDTH, -CAR_WIDTH]

# AI contants
LIVING_PENALTY = 0.9
INPUT_SIZE = 5 # refers to 3 sensors + 2 orientations (positive and negative)

WORST_REWARD = -1
BAD_REWARD = -0.2
GOOD_REWARD = 0.1
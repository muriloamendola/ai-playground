from enum import Enum
from kivy.vector import Vector
from collections import namedtuple


Position = namedtuple('Position', ['x', 'y'])

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

DISTANCE_TO_REACH_GOAL = 100

EDGE_SIZE = 10

# AI contants
LIVING_PENALTY = 0.9
LEARNING_RATE = 0.001
INPUT_SIZE = 5 # refers to 3 sensors + 2 orientations (positive and negative)

WORST_REWARD = -1
BAD_REWARD = -0.2
GOOD_REWARD = 0.1

QTY_NEURONS = 30

REPLAY_MEMORY_SIZE = 100000
MIN_MEMORY_SIZE_TO_START_LEARN = 100

TEMPERATURE = 100 # To scale precision. The higher temperature the higher precision
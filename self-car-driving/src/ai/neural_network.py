import torch.nn as nn
from src.constants import QTY_NEURONS

class NeuralNetwork(nn.Module):
  def __init__(self, input_size, output_size):
    super(NeuralNetwork, self).__init__()
    
    # Define the layers
    self.input_layer = nn.Linear(input_size, QTY_NEURONS) 
    self.hidden_layer = nn.Linear(QTY_NEURONS, QTY_NEURONS)
    self.output_layer = nn.Linear(QTY_NEURONS, output_size)
    
    # Define activation functions (e.g., ReLU) for the hidden layers
    self.relu = nn.ReLU()

  def forward(self, state):
    """
    Forward pass through the layers with activation functions
    """
    state = self.relu(self.input_layer(state))
    state = self.relu(self.hidden_layer(state))
    return self.output_layer(state) # q_values

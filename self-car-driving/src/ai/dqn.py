import torch
import torch.optim as optim
import torch.nn.functional as F

from src.ai.replay_memory import ReplayMemory
from src.ai.neural_network import NeuralNetwork

from src.constants import LEARNING_RATE
from src.constants import REPLAY_MEMORY_SIZE
from src.constants import TEMPERATURE
from src.constants import MIN_MEMORY_SIZE_TO_START_LEARN


class Dqn():
  """
  Deep Q-Learning implementation
  """    
  def __init__(self, input_size, output_size, gamma):
    self.gamma = gamma
    self.model = NeuralNetwork(input_size, output_size)
    self.memory = ReplayMemory(REPLAY_MEMORY_SIZE)
    self.optimizer = optim.Adam(self.model.parameters(), lr=LEARNING_RATE)
    self.last_state = torch.Tensor(input_size).unsqueeze(0)
    self.last_action = 0
    self.last_reward = 0
    
  def select_action(self, state):
    """
    By adjusting the temperature parameter, you can control the trade-off between exploration and exploitation. 
    Higher temperatures encourage more exploration, while lower temperatures encourage more exploitation of the 
    current best-known actions based on Q-values.
    """
    q_values = self.model(state)
    action_probs = F.softmax(q_values*TEMPERATURE, dim=1)
    action = torch.multinomial(input=action_probs, num_samples=1).item()
    return action
    
  def learn(self, batch_state, batch_next_state, batch_reward, batch_action):
    # Pass your input data through the model to get predictions.
    outputs = self.model(batch_state).gather(1, batch_action.unsqueeze(1)).squeeze(1)
    next_outputs = self.model(batch_next_state).detach().max(1)[0]
    target = self.gamma*next_outputs + batch_reward

    # Compute the loss using the predicted values and the target values.
    loss = F.smooth_l1_loss(outputs, target)

    # clear gradients
    self.optimizer.zero_grad()

    # Backpropagation
    loss.backward(retain_graph = True)    
    self.optimizer.step()
  
  def _build_new_memory_event(self, new_state) -> tuple:
    """
    Memory events are a tuple, where:
    - first element is the last state of the agent
    - second element is the new state
    - thrid element is the last agent action
    - fourth element is the last reward owned
    """
    last_action_tensor = torch.LongTensor([int(self.last_action)])
    last_reward_tensor = torch.Tensor([self.last_reward])

    return (self.last_state, new_state, last_action_tensor, last_reward_tensor)

  def _checks_if_has_to_start_learn(self):
    has_to_learn = len(self.memory.memory) > MIN_MEMORY_SIZE_TO_START_LEARN
    if has_to_learn:
      batch_state, batch_next_state, batch_action, batch_reward = self.memory.sample(MIN_MEMORY_SIZE_TO_START_LEARN)
      self.learn(batch_state, batch_next_state, batch_reward, batch_action)

  def update(self, reward, new_signal):
    new_state = torch.Tensor(new_signal).float().unsqueeze(0)
    self.memory.push(self._build_new_memory_event(new_state))
    action = self.select_action(new_state)

    self._checks_if_has_to_start_learn()

    self.last_action = action
    self.last_state = new_state
    self.last_reward = reward
    
    return action

# Deep Q-Learning Car Control App

This Python application uses Deep Q-Learning to control a virtual car, enabling it to learn a path between two points and dodge obstacles. The graphical user interface is built with Kivy, making it easy to interact with and visualize the car's progress.

> This project was created for study purpose and was inspired on the training [Artificial Intelligence A-Z™ 2023: Build an AI with ChatGPT4
](https://www.udemy.com/course/artificial-intelligence-az/learn/lecture/7138844#overview).

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Deep Q-Learning](#deep-q-learning)
- [Temperature Parameter](#temperature-parameter)
- [Neural Network Architecture](#neural-network-architecture)
- [Replay Memory](#replay-memory)
- [Sample](#sample)

## Introduction

This project showcases the implementation of Deep Q-Learning, a popular reinforcement learning technique, to control a car's navigation in a simulated environment. The car learns to find the optimal path between two given points while avoiding obstacles. Here, we provide an overview of the AI concepts and components used in this project.

## Getting Started

To run the application, you'll need Python and the following dependencies:

- Kivy: A Python framework for developing multitouch applications.
- PyTorch: An open-source machine learning library.

You can install these dependencies using `pip`:

```bash
pip install -r requirements.txt
```

Once the dependencies are installed, you can run the application by executing the main script.

```bash
python main.py
```

## Deep Q-Learning

Deep Q-Learning (DQL) is a reinforcement learning technique used to train agents to make decisions in an environment. In this project, the DQL algorithm is employed to teach the car how to navigate from one point to another while avoiding obstacles. Key components of the DQL algorithm used in this project include:

### Neural Network Architecture

The neural network, implemented using PyTorch, serves as the Q-function approximator. It takes the current state of the environment as input and outputs Q-values for each possible action. The neural network architecture can be found in the [NeuralNetwork class](./src/ai/neural_network.py) in the code.

### Replay Memory

To stabilize training and improve sample efficiency, the application uses a replay memory. This memory stores past experiences, allowing the agent to learn from a random sample of these experiences during training. The [ReplayMemory class](./src/ai/replay_memory.py) in the code handles the management of replay memory.

### Temperature Parameter

The temperature parameter in the select_action function controls the trade-off between exploration and exploitation. Higher temperatures encourage more exploration of actions, while lower temperatures favor exploitation of the current best-known actions based on Q-values.

> Fell free to tunning the learning process, changing values inside [constants.py file](./src/constants.py).

## Sample

![Sample runnning](sample.gif)
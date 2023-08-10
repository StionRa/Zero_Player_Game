"""
ai_character_model.py

This module defines the AICharacterModel class and its related components for training and using
a reinforcement learning model to control game characters.

Classes:
    DQN: Deep Q-Network neural network architecture.
    AICharacterModel: Class representing the AI character model for training and decision-making.

Functions:
    None

Usage example:
    character_model = AICharacterModel(input_size, output_size)
    character_model.train_batch(batch, done, character)
    action = character_model.get_action(state)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import h5py
import numpy as np

# List of available actions
actions_list = [
    "strike_with_a_hand",
    "skip_a_turn",
]

# Action dictionary definition
actions_dict = {
    0: "strike_with_a_hand",
    1: "skip_a_turn",
}

# The size of the input data and the number of possible actions
input_size = 8
output_size = len(actions_list)


class DQN(nn.Module):  # Neural network
    """
    Deep Q-Network neural network architecture.
    """
    def __init__(self, input_size, output_size):
        """
        :type input_size: int
        :param input_size: 8
        :param output_size: 2
        """
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, output_size)

    def forward(self, x):  # Forward propagation
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def save_model_state_to_hdf5(self, file_path):  # Save the model's state to a file
        """
        Save the model's state dictionary to an HDF5 file.
        Args:
            file_path (str): Path to the file to save the model's state to.
        """
        state_dict = self.state_dict()
        # Convert the model's parameters to native data types
        converted_state_dict = {key: value.cpu().numpy() for key, value in state_dict.items()}

        with h5py.File(file_path, 'w') as hf:
            for key, value in converted_state_dict.items():
                hf.create_dataset(key, data=value)


class AICharacterModel:  # AI character model
    """
    Class representing the AI character model for training and decision-making.
    """
    def __init__(self, input_size, output_size, buffer_size=1000, batch_size=32):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DQN(input_size, output_size).to(self.device)
        self.target_model = DQN(input_size, output_size).to(self.device)
        self.target_model.load_state_dict(self.model.state_dict())
        self.target_model.eval()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        self.loss_fn = nn.MSELoss()

        # Experience Replay buffer
        self.buffer_size = buffer_size
        self.batch_size = batch_size
        self.buffer = []

    def update_target_model(self):  # Update the target model
        self.target_model.load_state_dict(self.model.state_dict())

    def save_model_state_to_hdf5(self, file_path):  # Save the model's state to a file
        state_dict = self.model.state_dict()
        # Convert the model's parameters to native data types
        converted_state_dict = {key: value.cpu().numpy() for key, value in state_dict.items()}

        with h5py.File(file_path, 'w') as hf:
            for key, value in converted_state_dict.items():
                hf.create_dataset(key, data=value)

    def load_model_state_from_hdf5(self, file_path):    # Load the model's state from a file
        with h5py.File(file_path, 'r') as hf:
            state_dict_data = {key: value[()] for key, value in hf.items()}

            # Convert the values to tensors individually
            state_dict_tensors = {key: torch.tensor(value) for key, value in state_dict_data.items()}

            # Load the state dictionary with tensors
            self.model.load_state_dict(state_dict_tensors)

    def get_action(self, state):    # Get action from model
        """
        Get the best action based on the current state.

        Args:
            state (list or array-like): The current state of the game environment.

        Returns:
            int: The chosen action index.
        """
        state_tensor = torch.tensor(state, dtype=torch.float).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.model(state_tensor)
        action = torch.argmax(q_values).item()
        return action

    def convert_to_tensors(self, batch, done):  # Convert batch to tensors
        """
        Convert the batch of experiences to PyTorch tensors.

        Args:
            batch (list): A list of tuples, each containing (state, next_state, action, reward).
            done (bool): Whether the episode is done or not.

        Returns:
            tuple: Tuple of PyTorch tensors (states, next_states, actions, rewards, dones).
        """
        states, next_states, actions, rewards = zip(*batch)
        states = np.array(states, dtype=np.float32)
        next_states = np.array(next_states, dtype=np.float32)
        actions = np.array(actions, dtype=np.int64)
        rewards = np.array(rewards, dtype=np.float32)

        states_tensor = torch.tensor(states).to(self.device)
        next_states_tensor = torch.tensor(next_states).to(self.device)
        actions_tensor = torch.tensor(actions).unsqueeze(1).to(self.device)
        rewards_tensor = torch.tensor(rewards).to(self.device)
        dones_tensor = torch.tensor(done, dtype=torch.float).to(self.device)

        return states_tensor, next_states_tensor, actions_tensor, rewards_tensor, dones_tensor

    def train_batch(self, batch, done, character):
        """
            Train the model using Deep Q-Learning and make decisions using the trained model.
            Args:
                batch (list): List of tuples containing the state, next state, action, and reward.
                done (bool): Whether the episode is done or not.
                character (Character): The character to make decisions for.
                """
        if not batch:
            return

        # Convert batch to tensors
        states_tensor, next_states_tensor, actions_tensor, rewards_tensor, dones_tensor = self.convert_to_tensors(batch,
                                                                                                                  done)

        with torch.no_grad():   # Get the target q-values
            next_q_values = self.target_model(next_states_tensor)
            target_q_values = rewards_tensor + (1 - dones_tensor) * 0.99 * next_q_values

        q_values = self.model(states_tensor)
        predicted_q_values = q_values.gather(1, actions_tensor).squeeze(1)
        loss = self.loss_fn(predicted_q_values, target_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.update_target_model()
        file_path = f'{character.name}_ai_model.h5'
        self.target_model.save_model_state_to_hdf5(file_path)
        # Print training progress
        print(f"{character.name} - Training progress - Model learning rate: {self.optimizer.param_groups[0]['lr']:.6f}")
        print(f"{character.name} - Loss: {loss.item():.6f}")

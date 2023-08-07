import torch
import torch.nn as nn
import torch.nn.functional as F
import h5py
import random

actions_list = [
    "strike_with_a_hand",
    "skip_a_turn",
]

# Определение списка действий
actions_dict = {
    0: "strike_with_a_hand",
    1: "skip_a_turn",
}


class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, output_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class AICharacterModel:
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

    def update_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())

    def save_model_state_to_hdf5(self, file_path):
        state_dict = self.model.state_dict()
        # Convert the model's parameters to native data types
        converted_state_dict = {key: value.cpu().numpy() for key, value in state_dict.items()}

        with h5py.File(file_path, 'w') as hf:
            for key, value in converted_state_dict.items():
                hf.create_dataset(key, data=value)

    def load_model_state_from_hdf5(self, file_path):
        with h5py.File(file_path, 'r') as hf:
            state_dict_data = {key: torch.tensor(value) for key, value in hf.items()}
            self.model.load_state_dict(state_dict_data)

    def get_action(self, state):
        state_tensor = torch.tensor(state, dtype=torch.float).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.model(state_tensor)
        action = torch.argmax(q_values).item()
        return action

    def train_batch(self, buffer, actions, rewards, next_states, dones, character):
        if not buffer:
            return

        states = torch.tensor(buffer, dtype=torch.float).to(self.device)
        actions = torch.tensor(actions, dtype=torch.long).unsqueeze(1).to(self.device)
        rewards = torch.tensor(rewards, dtype=torch.float).to(self.device)
        next_states = torch.tensor(next_states, dtype=torch.float).to(self.device)
        dones = torch.tensor(dones, dtype=torch.float).to(self.device)

        with torch.no_grad():
            next_q_values = self.target_model(next_states)
            target_q_values = rewards + (1 - dones) * 0.99 * next_q_values

        q_values = self.model(states)
        predicted_q_values = q_values.gather(1, actions).squeeze(1)
        loss = self.loss_fn(predicted_q_values, target_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.update_target_model()
        file_path = f'{character.name}_ai_model.h5'
        self.target_model.save_model_state_to_hdf5(file_path)
        # Print training progress
        print("Training batch...")
        print(f"Loss: {loss.item()}")
        print(f"Original > Model state saved to {character.name}_ai_model.h5")

    def train(self, states, actions, rewards, next_states, dones, character):
        # Store the experience in the buffer
        self.buffer.append((states, actions, rewards, next_states, dones))
        if len(self.buffer) > self.buffer_size:
            # Remove old experience if buffer size exceeds the limit
            self.buffer.pop(0)

        if len(self.buffer) >= self.batch_size:
            # Sample a random batch of experiences from the buffer
            batch = random.sample(self.buffer, self.batch_size)
            batch_states, batch_actions, batch_rewards, batch_next_states, batch_dones = zip(*batch)
            self.train_batch(batch_states, batch_actions, batch_rewards, batch_next_states, batch_dones, character)
            file_path = f'{character.name}_ai_model.h5'
            self.target_model.save_model_state_to_hdf5(file_path)

            print(f"Double > Model state saved to {character.name}_ai_model.h5")

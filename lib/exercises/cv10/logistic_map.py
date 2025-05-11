import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm

def logistic_map(x, a):
    return a * x * (1 - x)

def generate_bifurcation_data(a_min=2.5, a_max=4.0, num_a_values=1000, 
                             num_iterations=1000, num_discard=800):
    a_values = np.linspace(a_min, a_max, num_a_values)
    x_values = []
    a_for_points = []
    
    for a in tqdm(a_values, desc="Generuji bifurkační data"):
        x = 0.5
        
        for _ in range(num_discard):
            x = logistic_map(x, a)
        
        for _ in range(num_iterations - num_discard):
            x = logistic_map(x, a)
            x_values.append(x)
            a_for_points.append(a)
    
    return np.array(a_values), np.array(a_for_points), np.array(x_values)

def plot_bifurcation(a_for_points, x_values, title="Bifurkační diagram logistické mapy"):
    plt.figure(figsize=(10, 6))
    plt.scatter(a_for_points, x_values, s=0.1, color='blue', alpha=0.5)
    plt.xlabel('Parametr a')
    plt.ylabel('Stabilní body x')
    plt.title(title)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.show()

class LogisticMapPredictor(nn.Module):
    def __init__(self):
        super(LogisticMapPredictor, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(2, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
    
    def forward(self, x):
        return self.network(x)

def prepare_training_data(a_values, x_values, test_size=0.2):
    inputs = []
    targets = []
    
    for i in range(len(x_values) - 1):
        if a_values[i] == a_values[i+1]:
            inputs.append([x_values[i], a_values[i]])
            targets.append(x_values[i+1])
    
    inputs = np.array(inputs, dtype=np.float32)
    targets = np.array(targets, dtype=np.float32).reshape(-1, 1)
    
    split_idx = int(len(inputs) * (1 - test_size))
    X_train, X_test = inputs[:split_idx], inputs[split_idx:]
    y_train, y_test = targets[:split_idx], targets[split_idx:]
    
    return X_train, X_test, y_train, y_test

def train_model(model, X_train, y_train, X_test, y_test, batch_size=128, epochs=50):
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)
    
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    model.train()
    losses = []
    val_losses = []
    
    for epoch in range(epochs):
        epoch_loss = 0.0
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        
        model.eval()
        with torch.no_grad():
            val_outputs = model(X_test_tensor)
            val_loss = criterion(val_outputs, y_test_tensor).item()
            val_losses.append(val_loss)
        
        avg_loss = epoch_loss / len(train_loader)
        losses.append(avg_loss)
        
        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f'Epocha {epoch+1}/{epochs}, Ztráta: {avg_loss:.6f}, Validační ztráta: {val_loss:.6f}')
        
        model.train()
    
    return model, losses, val_losses

def generate_predictions(model, a_min=2.5, a_max=4.0, num_a_values=200, num_iterations=100):
    a_values = np.linspace(a_min, a_max, num_a_values)
    predictions = []
    a_for_predictions = []
    
    model.eval()
    with torch.no_grad():
        for a in tqdm(a_values, desc="Generuji predikce"):
            x = 0.5
            
            for _ in range(100):
                x = logistic_map(x, a)
            
            for _ in range(num_iterations):
                input_tensor = torch.tensor([[x, a]], dtype=torch.float32)
                x_pred = model(input_tensor).item()
                x = x_pred  # Použití predikce jako vstup pro další iteraci
                predictions.append(x)
                a_for_predictions.append(a)
    
    return np.array(a_for_predictions), np.array(predictions)

def run():
    print("Generuji bifurkační diagram...")
    a_values_full, a_points, x_points = generate_bifurcation_data(
        a_min=2.5, a_max=4.0, num_a_values=500, num_iterations=300, num_discard=200
    )
    
    plot_bifurcation(a_points, x_points)
    
    print("Připravuji trénovací data...")
    X_train, X_test, y_train, y_test = prepare_training_data(a_points, x_points)

    print("Trénuji neuronovou síť...")
    model = LogisticMapPredictor()
    trained_model, train_losses, val_losses = train_model(
        model, X_train, y_train, X_test, y_test, epochs=30
    )
    
    plt.figure(figsize=(10, 5))
    plt.plot(train_losses, label='Trénovací ztráta')
    plt.plot(val_losses, label='Validační ztráta')
    plt.xlabel('Epocha')
    plt.ylabel('Ztráta (MSE)')
    plt.title('Průběh trénování modelu')
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    print("Generuji predikce pomocí neuronové sítě...")
    a_pred, x_pred = generate_predictions(
        trained_model, a_min=2.5, a_max=4.0, num_a_values=200, num_iterations=100
    )
    
    plt.figure(figsize=(12, 8))    
    plt.subplot(2, 1, 1)
    plt.scatter(a_points, x_points, s=0.1, color='blue', alpha=0.5)
    plt.xlabel('Parametr a')
    plt.ylabel('Hodnoty x')
    plt.title('Skutečná data logistické mapy')
    plt.ylim(0, 1)    
    plt.subplot(2, 1, 2)
    plt.scatter(a_pred, x_pred, s=0.1, color='red', alpha=0.5)
    plt.xlabel('Parametr a')
    plt.ylabel('Hodnoty x')
    plt.title('Predikce neuronové sítě')
    plt.ylim(0, 1)    
    plt.tight_layout()
    plt.show()
import torch
from torch import nn
from torch.utils.data import DataLoader
from main import UrbanSoundDataset
import torchaudio
from cnn import CNNetwork



SAMPLE_RATE = 22050
NUM_SAMPLES = 22050
ANNOTATIONS_FILE = "C:\\Users\\micah\\PycharmProjects\\pythonProject9\\SpotifySongs\\songs_data.csv"
AUDIO_DIR = "C:\\Users\\micah\\PycharmProjects\\pythonProject9\\SpotifySongs\\mp3_files"
BATCH_SIZE = 64
EPOCHS = 10
LEARNING_RATE = 0.00000155
def create_data_loader(train_data, batch_size):
    train_dataloader = DataLoader(train_data, batch_size=batch_size)
    return  train_dataloader
def train_one_epoch(model, data_loader, loss_fn, optimiser, device):
    model.train()
    correct = 0
    total = 0
    for inputs, targets in data_loader:
        inputs, targets = inputs.to(device), targets.to(device)

        # Forward pass
        predictions = model(inputs)
        loss = loss_fn(predictions, targets)

        # Backward pass and optimization
        optimiser.zero_grad()
        loss.backward()
        optimiser.step()

        _, predicted = torch.max(predictions, 1)
        total += targets.size(0)
        correct += (predicted == targets).sum().item()

    accuracy = correct / total
    print(f"Loss: {loss.item()}, Accuracy: {accuracy * 100}%")



def train(model, data_loader, loss_fn, optimiser, device, epochs):
    for i in range(epochs):
        print(f"Epoch {i+1}")
        train_one_epoch(model, data_loader, loss_fn, optimiser, device)
        print("\n Training")



if __name__ == "__main__":
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    print(f"using {device}")


# Initialize stuff
    mel_spectogram = torchaudio.transforms.MelSpectrogram(sample_rate=SAMPLE_RATE, n_fft=1024, hop_length=512, n_mels=64)

    mel_spectrogram = mel_spectogram.to(device)

    usd = UrbanSoundDataset(ANNOTATIONS_FILE, AUDIO_DIR, mel_spectogram, SAMPLE_RATE, NUM_SAMPLES, device)

    train_data_loader = DataLoader(usd, batch_size=BATCH_SIZE)
 #Constructs model
    cnn = CNNetwork().to(device)

# Initialize LF + Optimiser
    loss_fn = nn.CrossEntropyLoss()


    optimiser = torch.optim.Adam(cnn.parameters(), lr=LEARNING_RATE)

    # Train
    train(cnn, train_data_loader, loss_fn, optimiser, device, EPOCHS)


    # Save
    torch.save(cnn.state_dict(), "trained.pth")
    print("Model Trained and stored at trained.pth")
    cnn.eval()

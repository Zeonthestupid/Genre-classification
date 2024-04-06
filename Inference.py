import torch
from cnn import CNNetwork
import torchaudio
from main import UrbanSoundDataset
import pandas as pd
import random
SAMPLE_RATE = 22050
NUM_SAMPLES = 22050
device = "cuda"
ANNOTATIONS_FILE = "C:\\Users\\micah\\PycharmProjects\\pythonProject9\\SpotifySongs\\ref_data.csv"
AUDIO_DIR = "C:\\Users\\micah\\PycharmProjects\\pythonProject9\\SpotifySongs\\mp3_files"


##
# "C:\\Users\\micah\\PycharmProjects\\pythonProject9\\UrbanSound8K\\audio"
# "C:\\Users\\micah\\PycharmProjects\\pythonProject9\\UrbanSound8K\\metadata\\UrbanSound8K.csv"
#
class_mapping_two = [
    "air_conditioner",
    "car_horn",
    "children_playing",
    "dog_bark",
    "drilling",
    "engine_idling",
    "gun_shot",
    "jackhammer",
    "siren",
    "street_music"
]

def predict(model, input, target, class_mapping):
    model.eval()
    with torch.no_grad():
        predictions = model(input)
        predicted_index = predictions[0].argmax(0)
        predicted = class_mapping[predicted_index]
        expected = class_mapping[target]
        print (f"predicted: {predicted} expected: {expected}")
    return predicted, expected
if __name__ == "__main__":
    class_mapping = []
    with open('classes.txt', 'r') as file:
        for line in file:
            class_name = line.strip().split(' - ')[1]
            class_mapping.append(class_name)

    x = input("Just to wait")
    cnn = CNNetwork()
    state_dict = torch.load("trained.pth")
    cnn.load_state_dict(state_dict)
    cnn = cnn.to(device)
    mel_spectogram = torchaudio.transforms.MelSpectrogram(sample_rate=SAMPLE_RATE, n_fft=1024, hop_length=512,
                                                          n_mels=64)
    mel_spectrogram = mel_spectogram.to(device)

    usd = UrbanSoundDataset(ANNOTATIONS_FILE, AUDIO_DIR, mel_spectogram, SAMPLE_RATE, NUM_SAMPLES, device)
    file_index = 1
    incorrect_predictions = 0
    correct_predictions = 0
    tests_run = len(pd.read_csv(ANNOTATIONS_FILE)) - 2
    for _ in range(tests_run):
        input, target = usd[file_index][0], usd[file_index][1]
        input.unsqueeze_(0)
        file_index += 1
        predicted, expected = predict(cnn, input, target, class_mapping)
        print (f"Prediction: {predicted}, Expected: {expected}")
        if predicted == expected:
            correct_predictions += 1
        else:
            incorrect_predictions +=1

    print (f"{correct_predictions} | {incorrect_predictions} ({correct_predictions/tests_run * 100}%)")
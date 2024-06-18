import os
import pickle

class Settings():
    def __init__(self):
        self.initial_audio_dir = "/Users/geoffyli/Library/CloudStorage/GoogleDrive-lyl1719770869@gmail.com/My Drive/Courses/TOEFL/23托福听力真题/23托福听力机经"
        self.export_folder_path = ""
        self.sentence_counter = 0

    @staticmethod
    def load(filename="settings.pkl"):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                return pickle.load(f)
        return Settings()

    def save(self, filename="settings.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)


settings = Settings.load()
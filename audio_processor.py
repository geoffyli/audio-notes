# pydub
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import assemblyai as aai
import threading
import os

aai.settings.api_key = "0d3d110e7c34441c83126e4e5a74cdf6"


class AudioProcessor:
    def __init__(self):
        self.audio_path = None
        self.audio = None
        self.transcriber = aai.Transcriber()
        self.transcript = None
        self.sentences = None
        self.lock = threading.Lock()

    def load_audio(self, audio_path):
        self.audio_path = audio_path
        self.audio = AudioSegment.from_file(audio_path)

    def transcribe(self):
        # transcribe the file
        self.transcript = self.transcriber.transcribe(self.audio_path)
        self.sentences = self.transcript.get_sentences()
        return self.sentences

    def play_audio_segment(self, start: int, end: int):
        # Attempt to acquire the lock
        if not self.lock.acquire(timeout=0):
            return
        try:
            # Slice audio
            audio_segment = self.audio[start:end]
            # Temporary file
            with tempfile.NamedTemporaryFile(delete=True) as temp:
                # Export audio segment to temporary file
                audio_segment.export(temp.name, format="wav")
                # Load exported audio segment
                exported_segment = AudioSegment.from_wav(temp.name)
                # Play audio
                play(exported_segment)
        finally:
            # Make sure to release the lock, even in case of error.
            self.lock.release()

    def export_audio_segment(self, start: int, end: int, folder_path: str, filename:str):
        # Slice audio
        audio_segment = self.audio[start:end]
        # Concat full path
        full_path = os.path.join(folder_path, filename)
        # Export mp3 file
        audio_segment.export(full_path, format="mp3")

from pydub import AudioSegment
from pydub.playback import play
import tempfile


def play_audio_segment(file_path: str, start: int, end: int):
    # Load the audio file
    audio = AudioSegment.from_wav(file_path)

    # Convert start and end from seconds to milliseconds
    start *= 1000
    end *= 1000

    # Slice audio
    audio_segment = audio[start:end]

    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=True) as temp:
        # Export audio segment to temporary file
        audio_segment.export(temp.name, format="wav")
        
        # Load exported audio segment
        exported_segment = AudioSegment.from_wav(temp.name)

        # Play audio
        play(exported_segment)


play_audio_segment("test.wav", 90, 110)

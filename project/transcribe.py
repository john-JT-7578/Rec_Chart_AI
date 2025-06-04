import whisper

model = whisper.load_model('base')


def transcribe_audio(path: str) -> str:
    """Transcribe an audio file using Whisper."""
    result = model.transcribe(path)
    return result['text']

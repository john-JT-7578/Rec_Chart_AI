"""Utilities for running Whisper transcription."""

try:
    import whisper  # type: ignore
except Exception as exc:  # pragma: no cover - handled at runtime
    whisper = None  # type: ignore
    _load_error = exc
else:
    _load_error = None

_model = None


def _get_model():
    """Load the Whisper model on first use."""
    global _model
    if whisper is None:
        raise RuntimeError(
            "Whisper library failed to load. Ensure 'openai-whisper' is installed" 
            f" ({_load_error})"
        )
    if _model is None:
        _model = whisper.load_model("base")
    return _model


def transcribe_audio(path: str) -> str:
    """Transcribe an audio file using Whisper."""
    model = _get_model()
    result = model.transcribe(path)
    return result["text"]

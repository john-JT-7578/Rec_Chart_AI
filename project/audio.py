import queue
import threading
import time
import numpy as np
import sounddevice as sd
import soundfile as sf
from datetime import datetime
from pathlib import Path


audio_queue = queue.Queue()
recording = False


def _callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())


def start_recording(samplerate=16000, channels=1):
    global recording
    recording = True
    stream = sd.InputStream(callback=_callback, channels=channels, samplerate=samplerate)
    stream.start()
    return stream


def stop_recording(stream, output_dir="recordings"):
    global recording
    recording = False
    stream.stop()
    stream.close()
    Path(output_dir).mkdir(exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = Path(output_dir) / f"chunk_{timestamp}.wav"
    frames = []
    while not audio_queue.empty():
        frames.append(audio_queue.get())
    if frames:
        data = np.concatenate(frames, axis=0)
        sf.write(filename, data, samplerate=stream.samplerate)
        return str(filename)
    return None


def record_chunk(duration=5, samplerate=16000, channels=1, output_dir="recordings"):
    """Record a single audio chunk and return the saved path."""
    # clear leftover frames
    while not audio_queue.empty():
        audio_queue.get()
    stream = start_recording(samplerate=samplerate, channels=channels)
    time.sleep(duration)
    return stop_recording(stream, output_dir=output_dir)

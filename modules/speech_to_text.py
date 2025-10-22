"""
Speech-to-Text Module for AI Clinical Notes Assistant
Uses OpenAI Whisper for offline transcription
"""
import whisper
import sounddevice as sd
import soundfile as sf
import numpy as np
from pathlib import Path
import tempfile
import threading

class SpeechToText:
    def __init__(self, model_name="base"):
        """
        Initialize Whisper model
        Args:
            model_name: Whisper model size (tiny, base, small, medium, large)
        """
        self.model_name = model_name
        self.model = None
        self.is_recording = False
        self.recorded_audio = []
        self.sample_rate = 16000

    def load_model(self):
        """Load Whisper model (lazy loading)"""
        if self.model is None:
            try:
                self.model = whisper.load_model(self.model_name)
                return True
            except Exception as e:
                print(f"Error loading Whisper model: {e}")
                return False
        return True

    def transcribe_file(self, audio_path):
        """
        Transcribe audio file
        Args:
            audio_path: Path to audio file (wav, mp3, etc.)
        Returns:
            Transcribed text or None if error
        """
        if not self.load_model():
            return None

        try:
            result = self.model.transcribe(str(audio_path))
            return result['text'].strip()
        except Exception as e:
            print(f"Error transcribing file: {e}")
            return None

    def record_audio(self, duration=None, callback=None):
        """
        Record audio from microphone
        Args:
            duration: Recording duration in seconds (None for manual stop)
            callback: Callback function to update UI
        Returns:
            Path to saved audio file
        """
        self.is_recording = True
        self.recorded_audio = []

        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Recording status: {status}")
            if self.is_recording:
                self.recorded_audio.append(indata.copy())
                if callback:
                    callback(len(self.recorded_audio) * frames / self.sample_rate)

        try:
            with sd.InputStream(samplerate=self.sample_rate, channels=1,
                               callback=audio_callback, dtype=np.float32):
                if duration:
                    sd.sleep(int(duration * 1000))
                else:
                    # Wait until recording is stopped manually
                    while self.is_recording:
                        sd.sleep(100)

            # Save recorded audio
            if self.recorded_audio:
                audio_data = np.concatenate(self.recorded_audio, axis=0)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                sf.write(temp_file.name, audio_data, self.sample_rate)
                return temp_file.name
            return None

        except Exception as e:
            print(f"Error recording audio: {e}")
            self.is_recording = False
            return None

    def start_recording(self, callback=None):
        """
        Start recording audio in a separate thread
        Args:
            callback: Callback function to update UI with recording progress
        Returns:
            Recording thread
        """
        def record():
            self.recorded_audio = []
            self.is_recording = True

            def audio_callback(indata, frames, time, status):
                if status:
                    print(f"Recording status: {status}")
                if self.is_recording:
                    self.recorded_audio.append(indata.copy())
                    if callback:
                        duration = len(self.recorded_audio) * frames / self.sample_rate
                        callback(duration)

            try:
                with sd.InputStream(samplerate=self.sample_rate, channels=1,
                                   callback=audio_callback, dtype=np.float32):
                    while self.is_recording:
                        sd.sleep(100)
            except Exception as e:
                print(f"Error in recording thread: {e}")
                self.is_recording = False

        thread = threading.Thread(target=record, daemon=True)
        thread.start()
        return thread

    def stop_recording(self):
        """
        Stop recording and save audio file
        Returns:
            Path to saved audio file
        """
        self.is_recording = False
        sd.sleep(200)  # Wait for callback to finish

        if self.recorded_audio:
            try:
                audio_data = np.concatenate(self.recorded_audio, axis=0)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                sf.write(temp_file.name, audio_data, self.sample_rate)
                return temp_file.name
            except Exception as e:
                print(f"Error saving recorded audio: {e}")
                return None
        return None

    def transcribe_recording(self, audio_path):
        """
        Transcribe a recorded audio file
        Args:
            audio_path: Path to audio file
        Returns:
            Transcribed text
        """
        return self.transcribe_file(audio_path)

    def get_available_devices(self):
        """Get list of available audio input devices"""
        try:
            devices = sd.query_devices()
            input_devices = []
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    input_devices.append({
                        'id': i,
                        'name': device['name'],
                        'channels': device['max_input_channels']
                    })
            return input_devices
        except Exception as e:
            print(f"Error querying devices: {e}")
            return []

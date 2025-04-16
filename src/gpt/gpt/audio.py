#!/usr/bin/env python3
import os
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import sounddevice as sd
from ament_index_python.packages import get_package_share_directory
from pygame import mixer
import wave
import openai
from openai import OpenAI
from dotenv import load_dotenv
import subprocess

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
package_share_directory = get_package_share_directory('gpt')
audio_files_path = os.path.join(package_share_directory, 'audio_files')

def record_audio(duration=3, sample_rate=16000):
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    file_path = os.path.join(audio_files_path, 'recording.wav')
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)  # 16-bit audio
    wf.setframerate(sample_rate)
    wf.writeframes(recording.tobytes())
    wf.close()
    return file_path

def speech_to_text(wav_file_path):
    with open(wav_file_path, 'rb') as audio_file:
        transcription = openai.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            prompt="There are only 2 languages spoken: English & Indonesian."
        )
    return transcription.text

def text_to_speech(text, filename=None):
    try:
        if filename is None:
            filename = os.path.join(audio_files_path, "output.wav")
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
        )
        if not response:
            raise ValueError("No response from OpenAI API")
        response.stream_to_file(filename)

        fixed_filename = os.path.join(audio_files_path, "output_fixed.wav")
        subprocess.run([
            "ffmpeg", "-y", "-i", filename,
            "-ar", "44100", "-ac", "2", "-sample_fmt", "s16", fixed_filename
        ])
        return fixed_filename
    except Exception as e:
        return None

def play_audio(filename=os.path.join(audio_files_path, "output_fixed.wav")):
    if not os.path.exists(filename):
        return
    os.system(f"aplay {filename}")
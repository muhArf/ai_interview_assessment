# utils/speech_to_text.py
import speech_recognition as sr
from moviepy.editor import VideoFileClip
import os

def extract_audio_from_video(video_path):
    clip = VideoFileClip(video_path)
    audio_path = "temp_audio.wav"
    clip.audio.write_audiofile(audio_path, codec='pcm_s16le')
    return audio_path

def speech_to_text_from_video(video_path):
    recognizer = sr.Recognizer()
    audio_path = extract_audio_from_video(video_path)
    text_result = ""

    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text_result = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text_result = "(tidak dapat mengenali ucapan)"
        except sr.RequestError:
            text_result = "(gagal menghubungi API Speech Recognition)"

    os.remove(audio_path)
    return text_result

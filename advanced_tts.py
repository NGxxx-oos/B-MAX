from TTS.api import TTS
import sounddevice as sd
import numpy as np

# Инициализация модели (русский язык)
tts = TTS(model_name="tts_models/ru/ekaterina_v2", gpu=False)


def speak(text):
    # Генерация аудио
    audio = tts.tts(text)

    # Воспроизведение
    sd.play(audio, samplerate=22050)
    sd.wait()


# Пример
speak("Привет! Я ваш голосовой помощник с улучшенным голосом.")

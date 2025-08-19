import openai
import speech_recognition as sr
import pyttsx3

# Настройка OpenAI API (ключ на platform.openai.com)
openai.api_key = "api_ключ"

# Инициализация голосового движка
engine = pyttsx3.init()


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говорите...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="ru-RU")
            print(f"Вы сказали: {text}")
            return text
        except:
            return ""


def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]


def speak(text):
    engine.say(text)
    engine.runAndWait()


while True:
    user_input = listen()
    if user_input.lower() == "стоп":
        break

    if user_input:
        response = chat_with_gpt(user_input)
        print(f"Бот: {response}")
        speak(response)

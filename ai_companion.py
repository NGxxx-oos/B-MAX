import cv2
from deepface import DeepFace
import openai
import pyttsx3
import threading

# Настройка
openai.api_key = "api_ключ"
engine = pyttsx3.init()

current_emotion = "neutral"


def emotion_detection():
    global current_emotion
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            result = DeepFace.analyze(
                frame, actions=["emotion"], enforce_detection=False
            )
            current_emotion = result[0]["dominant_emotion"]
            cv2.putText(
                frame,
                f"Emotion: {current_emotion}",
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
        except:
            pass

        cv2.imshow("Emotion Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


def voice_chat():
    while True:
        user_input = input("Вы: ")  # Замена на голосовой ввод
        if user_input.lower() == "стоп":
            break

        # Запрос к ChatGPT
        prompt = f"Пользователь чувствует {current_emotion}. Ответь поддерживающе: {user_input}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
        )
        bot_response = response.choices[0].message["content"]
        print(f"Бот: {bot_response}")
        engine.say(bot_response)
        engine.runAndWait()


# Запуск в отдельных потоках
threading.Thread(target=emotion_detection, daemon=True).start()
voice_chat()

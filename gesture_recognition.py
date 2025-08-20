import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def recognize_gestures():
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
        max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7
    ) as hands:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                continue

            # Конвертация в RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            gesture = "none"

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Отрисовка landmarks
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )

                    # Анализ жестов
                    gesture = analyze_gesture(hand_landmarks)

                    cv2.putText(
                        frame,
                        f"Gesture: {gesture}",
                        (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                    )

            cv2.imshow("Gesture Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            yield gesture

    cap.release()
    cv2.destroyAllWindows()


def analyze_gesture(landmarks):
    # Получаем ключевые точки
    points = []
    for lm in landmarks.landmark:
        points.append([lm.x, lm.y])

    points = np.array(points)

    # Простые жесты
    thumb_tip = points[4]  # Кончик большого пальца
    index_tip = points[8]  # Кончик указательного
    middle_tip = points[12]  # Кончик среднего

    # Жест "ОК" (кольцо)
    if np.linalg.norm(thumb_tip - index_tip) < 0.05:
        return "ok"

    # Жест "Победа"
    if index_tip[1] < points[6][1] and middle_tip[1] < points[10][1]:
        return "victory"

    # Жест "Большой палец вверх"
    if thumb_tip[1] < points[2][1]:
        return "thumbs_up"

    return "unknown"

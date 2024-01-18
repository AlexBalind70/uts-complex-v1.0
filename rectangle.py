import cv2
import numpy as np
from tflite_runtime.interpreter import Interpreter

# Загрузка предварительно обученной модели
interpreter = Interpreter(model_path='rectangle_detection_model.tflite')  # Замените 'rectangle_detection_model.tflite' на ваш путь к модели
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_shape = input_details[0]['shape'][1:3]

# Функция для обработки кадра и распознавания прямоугольника
def process_frame(frame):
    # Преобразование кадра в формат, подходящий для входа в нейросеть
    frame = cv2.resize(frame, input_shape)
    frame = frame.reshape((1, *input_shape, 3))

    # Нормализация значений пикселей
    frame = frame / 255.0

    # Предсказание с использованием нейросети
    interpreter.set_tensor(input_details[0]['index'], frame)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]['index'])

    # Порог для определения, является ли объект прямоугольником
    threshold = 0.5
    if predictions[0][0] > threshold:
        return True
    else:
        return False

# Запуск видеопотока
cap = cv2.VideoCapture(0)  # Используйте 0 для веб-камеры, либо укажите путь к видеофайлу

while True:
    ret, frame = cap.read()

    if not ret:
        print("Не удалось получить кадр")
        break

    # Распознавание прямоугольника
    is_rectangle = process_frame(frame)

    # Отрисовка прямоугольника на кадре
    if is_rectangle:
        cv2.rectangle(frame, (50, 50), (200, 200), (0, 255, 0), 2)

    # Отображение результата
    cv2.imshow('Rectangle Detection', frame)

    # Прерывание при нажатии клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()

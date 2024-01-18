import cv2
import numpy as np
import time


def auto_canny(image, sigma=0.33):
    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    return edged


def sharpen(image):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(image, -1, kernel)
    return sharpened


def auto_focus(frame, threshold=1000):
    global prev_frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auto_edged = auto_canny(gray)
    cnts, _ = cv2.findContours(auto_edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) == 0:
        return frame

    c = max(cnts, key=cv2.contourArea)

    if cv2.contourArea(c) < threshold:
        return frame

    (x, y, w, h) = cv2.boundingRect(c)

    if prev_frame is not None:
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray[y:y + h, x:x + w], prev_gray[y:y + h, x:x + w])
        if np.mean(diff) < 10:
            return frame

    prev_frame = frame.copy()

    return frame[y:y + h, x:x + w]


cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

prev_frame = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    focused = auto_focus(frame)
    sharpened = sharpen(focused)

    cv2.imshow('Sharpened', sharpened)

    time.sleep(0.01)  # Задержка в 10 миллисекунд

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

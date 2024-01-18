import os
import types

import cv2 as cv
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog
from ui_file.complex_ui import Ui_MainWindow


class Microscope:
    def __init__(self):

        self.current_dir = None
        self.camera_1 = None
        self.is_camera1_opened = None
        self.ui = Ui_MainWindow()

    def start_camera(self):
        self.camera_1 = cv.VideoCapture(0)

        self.is_camera1_opened = ~self.is_camera1_opened
        self.ui.buttonAuto.setChecked(False)
        if self.is_camera1_opened:
            self._timer.start()
        else:
            self._timer.stop()

    @QtCore.pyqtSlot()
    def _queryFrame(self):
        circle_center_x = (635 + 2) // 2
        circle_center_y = 465 // 2
        try:
            gray = self._process_frame()

            ret, thresh = cv.threshold(gray, 125, 255, 0)
            contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            self._draw_and_annotate(
                contours=contours,
                circle_center_x=circle_center_x,
                circle_center_y=circle_center_y
            )

            self._draw_orange_circle_and_lines(
                circle_center_x=circle_center_x,
                circle_center_y=circle_center_y
            )

            self._display_processed_image()

        except Exception:
            self.camera_1.release()
            raise

    def _find_contours(self, frame):
        ret, thresh = cv.threshold(frame, 125, 255, 0)
        contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        return contours

    def _process_frame(self) -> np.ndarray:
        ret, self.frame = self.camera_1.read()

        if not ret or self.frame is None:
            # Handle the case where the frame is not successfully captured
            height = int(self.camera_1.get(cv.CAP_PROP_FRAME_HEIGHT))
            width = int(self.camera_1.get(cv.CAP_PROP_FRAME_WIDTH))
            return np.zeros((height, width), dtype=np.uint8)

        self.frame = cv.medianBlur(self.frame, 1)

        gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)

        noise = np.zeros(self.frame.shape, np.uint8)
        cv.randn(noise, 0, 25)
        self.frame = cv.add(self.frame, noise)

        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        self.frame = cv.filter2D(self.frame, -1, kernel)
        kernel = np.ones((3, 3), np.uint8)
        gradient = cv.morphologyEx(self.frame, cv.MORPH_GRADIENT, kernel)
        cv.add(self.frame, gradient)

        return gray

    def _draw_orange_circle_and_lines(self, circle_center_x: int, circle_center_y: int):
        color_orange = (0, 165, 255)
        color_yellow = (33, 255, 237)
        for i in range(1):
            cv.line(self.frame, (5, 230 + i), (635, 230 + i), color_yellow, thickness=2, lineType=8,
                    shift=0)
            cv.line(self.frame, (318 + i, 5), (318 + i, 470), color_yellow, thickness=2, lineType=8,
                    shift=0)
        cv.circle(self.frame, (circle_center_x, circle_center_y), 7, color_orange, -1)

    def _draw_and_annotate(self,
                           contours: tuple,
                           circle_center_x: int,
                           circle_center_y: int
                           ):
        color_blue = (255, 0, 0)
        for cnt in contours:
            x, y, w, h = cv.boundingRect(cnt)
            if w > 100 and h > 100:
                perc = 80  # Placeholder value; replace with the actual calculation
                label = "{:.2f}%".format(perc)

                font = cv.FONT_HERSHEY_SIMPLEX
                fontScale = 0.5
                thickness = 2
                size, _ = cv.getTextSize(label, font, fontScale, thickness)

                # Draw rectangle with filled blue color
                cv.rectangle(self.frame, (x, y - size[1]), (x + size[0], y), color_blue, cv.FILLED)

                # Draw bounding box
                rect = cv.minAreaRect(cnt)
                box = cv.boxPoints(rect)
                box = np.int0(box)
                cv.drawContours(self.frame, [box], 0, color_blue, 2)

                # Draw center of the bounding box
                center = (int(rect[0][0]), int(rect[0][1]))
                cv.circle(self.frame, center, 5, (0, 0, 255), -1)

                # Additional annotation (size label, distance calculation, etc.)
                size_label = "Size: {}x{}".format(w, h)
                cv.putText(self.frame, size_label, (x, y - size[1] - 10), font, fontScale, color_blue,
                           thickness)

                # Calculate the distance between the red point and the orange circle
                if self.ui.buttonAuto.isChecked():
                    self._set_auto(
                        center=center,
                        circle_center_x=circle_center_x,
                        circle_center_y=circle_center_y,
                        font=font
                    )

    def _display_processed_image(self):
        img_rows, img_cols, channels = self.frame.shape
        bytesPerLine = channels * img_cols

        cv.cvtColor(self.frame, cv.COLOR_BGR2RGB, self.frame)
        QImg = QImage(self.frame.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
        self.ui.cameraLabel.setPixmap(
            QPixmap.fromImage(QImg).scaled(
                self.ui.cameraLabel.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )
        self.ui.cameraLabel_2.setPixmap(
            QPixmap.fromImage(QImg).scaled(
                self.ui.cameraLabel_2.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

    def _set_auto(self, center: tuple, circle_center_x: int, circle_center_y: int, font: int) -> None:
        """
        Set auto parameters and display information on the frame.

        Parameters:
            center (tuple): Tuple representing the coordinates of the center.
            circle_center_x (int): X-coordinate of the circle center.
            circle_center_y (int): Y-coordinate of the circle center.
            font (int): Font type for displaying text.

        Returns:
            None
        """
        distance_x = circle_center_x - center[0]
        distance_y = circle_center_y - center[1]
        distance = np.sqrt(distance_x ** 2 + distance_y ** 2)

        font_scale = 0.5
        thickness = 2
        labels = [
            "Distance: {:.2f}".format(distance),
            "Move info line 1",
            "Move info line 2",
            "Red Point: ({}, {})".format(center[0], center[1]),
            "Orange Circle: ({}, {})".format(circle_center_x, circle_center_y)
        ]

        max_text_width = 0
        total_text_height = 0

        for label in labels:
            size, _ = cv.getTextSize(label, font, font_scale, thickness)
            max_text_width = max(max_text_width, size[0])
            total_text_height += size[1] + 10

        white_square = np.ones((total_text_height, max_text_width, 3), dtype=np.uint8) * 255
        white_square[:, :] = (255, 0, 255)

        move_info = "Move right " if distance_x > 0 else "Move left "
        move_info += "and move down." if distance_y > 0 else "and move up."
        labels.append(move_info)
        white_square.copy()

        current_height = 2
        current_width = 10
        self.frame[current_height:current_height + total_text_height,
        current_width:current_width + max_text_width] = white_square

        current_height = 20
        for label in labels:
            cv.putText(self.frame, label, (current_width, current_height), font, font_scale, (0, 0, 0), thickness)
            current_height += cv.getTextSize(label, font, font_scale, thickness)[1] + 10

    def take_snapshot(self) -> None:
        print('take_snapshot() called')
        file_name, _ = QFileDialog.getSaveFileName(self.ui.centralwidget, "Save Snapshot",
                                                   self.current_dir, "JPEG (*.jpg);;PNG (*.png)")

        if file_name:
            file_path = os.path.join(self.current_dir, file_name)
            cv.imwrite(file_path, self.frame)

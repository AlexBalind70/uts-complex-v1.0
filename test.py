import sys
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from complex_main import MainWindow


class MyTextTestResult(unittest.TextTestResult):
    def printErrors(self):
        pass


class MyTextTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return MyTextTestResult(self.stream, self.descriptions, self.verbosity)


class TestMainWindow(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.test_progress = {}

    def tearDown(self):
        self.window.close()

    def print_test_progress(self):
        total_tests = self.countTestCases()
        passed_tests = len([result for result in self.test_progress.values() if result])
        success_percentage = (passed_tests / total_tests) * 100
        print(f"\nTest completion: {success_percentage:.2f}% ({passed_tests}/{total_tests} tests passed)")

    def record_test_progress(self, test_name, result):
        self.test_progress[test_name] = result
        self.print_test_progress()

    def click_and_print(self, button):
        QTest.mouseClick(button, Qt.LeftButton)
        print(f"Button {button.objectName()} clicked")

    def test_initialization(self):
        self.assertIsNotNone(self.window)
        self.record_test_progress('test_initialization', True)

    def test_camera_toggle(self):
        self.assertFalse(self.window.is_camera1_opened)
        self.click_and_print(self.window.ui.cameraOn)
        self.assertTrue(self.window.is_camera1_opened)
        self.click_and_print(self.window.ui.cameraOn)
        self.assertFalse(self.window.is_camera1_opened)
        self.record_test_progress('test_camera_toggle', True)

    def test_movement_buttons(self):
        self.click_and_print(self.window.ui.buttonUp)
        self.click_and_print(self.window.ui.buttonDown)
        self.click_and_print(self.window.ui.buttonLeft)
        self.click_and_print(self.window.ui.buttonRight)
        self.record_test_progress('test_movement_buttons', True)

    def test_page_pagination(self):
        self.click_and_print(self.window.ui.buttonSettings)
        self.click_and_print(self.window.ui.buttonCameraControl)
        self.click_and_print(self.window.ui.buttonGenerator)
        self.click_and_print(self.window.ui.buttonVacuum)
        self.click_and_print(self.window.ui.buttonHistory)
        self.click_and_print(self.window.ui.buttonHome)
        self.record_test_progress('test_page_pagination', True)

    def test_lite_pagination(self):
        self.click_and_print(self.window.ui.LitebuttonSettings)
        self.click_and_print(self.window.ui.LitebuttonGenerator)
        self.click_and_print(self.window.ui.LitebuttonGenerator)
        self.click_and_print(self.window.ui.LitebuttonVacuum)
        self.click_and_print(self.window.ui.LitebuttonTable)
        self.click_and_print(self.window.ui.LitebuttonHistory)
        self.click_and_print(self.window.ui.LitebuttonHome)
        self.record_test_progress('test_lite_pagination', True)

    def test_save_graph(self):
        self.click_and_print(self.window.ui.buttonSaveGraph)
        self.record_test_progress('test_save_graph', True)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMainWindow)
    runner = MyTextTestRunner(verbosity=2)
    result = runner.run(suite)


from PyQt5.QtWidgets import QApplication


class Local_Language:

    def changeLanguage(self, index):
        if index == 0:
            # вызываем метод для установки английского языка
            self.trigger_english()
        elif index == 1:
            # вызываем метод для установки русского языка
            self.trigger_russian()

    # Локализация на английский язык
    def trigger_english(self):
        print('dddd')
        self.trans.load("app_en")
        _app = QApplication.instance()  # получить экземпляр приложения
        _app.installTranslator(self.trans)
        self.ui.retranslateUi(self)  # Перевести интерфейс
        pass

    # Локализация на русский язык
    def trigger_russian(self):
        self.trans.load("app_ru")
        _app = QApplication.instance()
        _app.installTranslator(self.trans)
        self.ui.retranslateUi(self)
        pass

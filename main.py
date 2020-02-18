import sys
from functools import partial

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (QRadioButton, QComboBox, QLabel, QTableWidget,
                             QTableWidgetItem)

from init import quiz, questions

class User:
    def __init__(self, name):
        self.name = name

class Game:
    def __init__(self):
        self.quiz = quiz
        self.questions = questions
        self.question_number = 1
        self.question_answers = {}

    @property
    def block_number(self):
        if self.question_number < 5:
            return 1
        elif self.question_number < 8:
            return 2
        elif self.question_number < 11:
            return 3
        elif self.question_number < 13:
            return 4
        else:
            return 5

    @property
    def block_str(self):
        if self.question_number < 5:
            return "Новачок"
        elif self.question_number < 8:
            return "Твердий початківець"
        elif self.question_number < 11:
            return "Компетентний"
        elif self.question_number < 13:
            return "Досвідчений"
        else:
            return "Експерт"

    def prev(self):
        if self.question_number != 1:
            self.question_number -= 1
        return self.questions[self.question_number-1]

    def next(self):
        if self.question_number != 16:
            self.question_number += 1
            return self.questions[self.question_number-1]
        else:
            return None


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.init_UI()
        self.UI_init_button_handlers()

    def init_UI(self):
        pass

    def UI_init_button_handlers(self):
        self.start_button.clicked.connect(self.start_quiz)
        self.start_button.clicked.connect(self.UI_update_info)
        self.next_question_button.clicked.connect(self.next_question)
        self.next_question_button.clicked.connect(self.UI_update_info)
        self.previous_question_button.clicked.connect(self.UI_update_info)

    def start_quiz(self):
        user_name = self.name_box.text()
        self.player = User(user_name)
        self.game = Game()

        self.views.setCurrentIndex(1)

    def UI_question_init(self, question):
        self.question_label.setText(question.title + '?')
        for i in range(3):
            radio = self.findChild(QRadioButton, f"radio{i+1}")
            radio.setText(list(question.answers.keys())[i])

    def UI_update_info(self):
        self.info_user_label.setText(f"Користувач - {self.player.name}")
        self.info_level_label.setText(f"Рівень - {self.game.question_number}")
        self.info_question_label.setText(f"Блок - {self.game.block_str}")

    def checked_radio_number(self):
        for i in range(3):
            radio = self.findChild(QRadioButton, f"radio{i+1}")
            if radio.isChecked():
                return i

    def evaluate_previous_question(self, answer_number):
        answers = list(self.game.questions[self.game.question_number-1].answers.values())
        answer_score = answers[answer_number]
        self.game.question_answers[self.game.question_number] = answer_score

    def next_question(self):
        self.evaluate_previous_question(self.checked_radio_number())
        next_question = self.game.next()
        if next_question:
            self.UI_question_init(next_question)
        else:
            print(self.game.question_answers)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

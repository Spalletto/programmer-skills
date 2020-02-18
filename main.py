import sys
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (QRadioButton, QLabel, QGridLayout)

from init import quiz, questions, blocks

class User:
    def __init__(self, name):
        self.name = name

class Game:
    def __init__(self):
        self.quiz = quiz
        self.questions = questions
        self.question_number = 1
        self.question_answers = {}

    def block_start_question(self):
        if self.question_number < 5:
            self.question_number = 1
        elif self.question_number < 8:
            self.question_number = 5
        elif self.question_number < 11:
            self.question_number = 8
        elif self.question_number < 13:
            self.question_number = 11
        else:
            self.question_number = 13

    @property
    def question(self):
        return self.questions[self.question_number]

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

        self.UI_init_button_handlers()

    def init_UI(self):
        pass

    def UI_init_plot(self):
        for block, (start, end) in blocks.items():
            layout_name = f"{block}_layout"
            x_labels = [f"Питання №{i+1}" for i in range(end - start + 1)]
            questions = list(range(start-1, end))
            answers = list(self.game.question_answers.values())[start-1:end]
            self.draw_bar_plot(questions, answers, x_labels, layout_name)

            label = self.findChild(QLabel, f"{block}_tab_label")
            label.setText(f"Ваш результат - {sum(answers)}")

        novice_answers = list(self.game.question_answers.values())[0:4]
        beginner_answers = list(self.game.question_answers.values())[4:7]
        competent_answers = list(self.game.question_answers.values())[7:10]
        proficient_answers = list(self.game.question_answers.values())[10:13]
        expert_answers = list(self.game.question_answers.values())[13:16]
        first_question = [novice_answers[0], beginner_answers[0], competent_answers[0], proficient_answers[0], expert_answers[0]]
        second_question = [novice_answers[1], beginner_answers[1], competent_answers[1], proficient_answers[1], expert_answers[1]]
        third_question = [novice_answers[2], beginner_answers[2], competent_answers[2], proficient_answers[2], expert_answers[2]]
        fourth_question = [novice_answers[3]]
        questions = [i for i, _ in enumerate(first_question)]
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.ax = self.figure.add_subplot(111)
        # self.ax.bar(questions[:-1], fourth_question, bottom=third_question +
        #             second_question+first_question, color='r')
        self.ax.bar(questions, third_question, bottom=second_question +
                    first_question, color='o')
        self.ax.bar(questions, second_question,
                    bottom=first_question, color='y')
        self.ax.bar(questions, first_question, color='g')
        #plt.xticks(questions, x_labels)
        layout = self.findChild(QGridLayout, layout_name)
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)

    def draw_bar_plot(self, x, y, x_labels, layout_name):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.ax = self.figure.add_subplot(111)
        self.ax.bar(x, y)
        plt.xticks(x, x_labels)
        layout = self.findChild(QGridLayout, layout_name)
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)

    def UI_init_button_handlers(self):
        self.start_button.clicked.connect(self.start_quiz)
        self.start_button.clicked.connect(self.UI_update_info)
        self.next_question_button.clicked.connect(self.next_question)
        self.next_question_button.clicked.connect(self.UI_update_info)
        self.previous_question_button.clicked.connect(self.previous_question)
        self.previous_question_button.clicked.connect(self.UI_update_info)
        self.restart_block_button.clicked.connect(self.restart_block)
        self.restart_block_button.clicked.connect(self.UI_update_info)

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
            self.UI_init_plot()
            self.views.setCurrentIndex(2)

    def previous_question(self):
        previous_question = self.game.prev()
        self.UI_question_init(previous_question)

    def restart_block(self):
        self.game.block_start_question()
        self.UI_question_init(self.game.question)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

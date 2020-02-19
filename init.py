class Question:
    def __init__(self, title: str, answers: dict):
        self.title = title
        self.answers = answers


class Block:
    def __init__(self, questions: list):
        self.questions = questions


class Quiz:
    def __init__(self, blocks: list):
        self.blocks = blocks

# novice
question1 = Question("Переживаєте за успіх в роботі", {u"Cильно": 5, u"Не дуже": 3, "Спокійний": 2})
question2 = Question("Прагнете досягти швидко результату", {"Поступово": 2, "Якомога швидше": 3, "Дуже": 5})
question3 = Question("Легко попадаєте в тупик при проблемах в роботі", {"Неодмінно": 5, "Поступово": 3, "Зрідка": 2})

# advanced beginner
question4 = Question("Чи використовуєте власний досвід при вирішенні задач", {"Зрідка": 5, "Частково": 3, "Ні": 2})
question5 = Question("Чи користуєтесь фіксованими правилами для вирішення задач", {"Так": 2, "В окремих випадках": 3, "Не потрібні": 5})
question6 = Question("Чи відчуваєте ви загальний контекст вирішення задачі", {"Так": 2, "Частково": 3, "В окремих випадках": 5})

# competent
question7 = Question("Чи можете ви побудувати модель вирішуваної задачі", {"Так": 5, "Не повністю": 3, "В окремих випадках": 2})
question8 = Question("Чи вистачає вам ініціативи при вирішенні задач", {"Так": 5, "Зрідка": 3, "Потрібне натхнення": 2})
question9 = Question("Чи можете вирішувати проблеми, з якими ще не стикались", {"Так": 2, "В окремих випадках": 3, "Ні": 5})

# proficient
question10 = Question("Чи необхідний вам весь контекст задачі", {"Так": 5, "В окремих деталях": 3, "В загальному": 2})
question11 = Question("Чи переглядаєте ви свої наміри до вирішення задачі", {"Так": 5, "Зрідка": 3, "Коли є потреба": 2})
question12 = Question("Чи здатні ви навчатись у інших", {"Так": 5, "Зрідка": 3, "Коли є потреба": 2})

# expert
question13 = Question("Чи обираєте ви нові методи своєї роботи", {"Так": 5, "Вибірково": 3, "Вистачає досвіду": 2})
question14 = Question("Чи допомагає власна інтуїція при вирішенні задач", {"Так": 5, "Частково": 3, "При емоційному напруженні": 2})
question15 = Question("Чи застовуєте рішення задач за аналогією", {"Часто": 5, "Зрідка": 3, "Тільки власний варіант": 2})

block1 = Block([question1, question2, question3])
block2 = Block([question4, question5, question6])
block3 = Block([question7, question8, question9])
block4 = Block([question10, question11, question12])
block5 = Block([question13, question14, question15])

quiz = Quiz([block1, block2, block3, block4, block5])
questions = [question1, question2, question3, question4, question5, question6, question7, question8, question9, question10, question11, question12, question13, question14, question15]
blocks = {'novice': (1, 3), 'beginner': (4, 6), 'competent': (7, 9), 'proficient': (10, 12), 'expert': (13, 15)}
block_names = ['Новачок', 'Твердий\n початківець', 'Компетентний', 'Продвинутий', 'Експерт']

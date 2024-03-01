import tkinter as tk
import random
import pygame


# Функция для чтения слов из файла
def read_words(filename):
    with open(filename, "r", encoding="utf-8") as file:
        words = [line.strip().split("=") for line in file]
    return words

# Класс карточки слова
class WordCard(tk.Label):
    def __init__(self, master, word, translation, app):
        super().__init__(master, text=word, font=("Arial", 24), bg="#ffffff", padx=20, pady=10, bd=2, relief="solid")  # Добавляем рамку
        self.word = word
        self.translation = translation
        self.app = app
        self.show_front = True
        self.bind("<Button-1>", self.flip_card)

    # Метод для переключения между видом слова и его переводом
    def flip_card(self, event):
        if self.show_front:
            self.config(text=self.translation, font=("Arial", 20), fg="#008000")
            self.show_front = False
        else:
            self.config(text=self.word, font=("Arial", 24), fg="#000000")
            self.show_front = True

# Класс приложения
class WordTrainerApp(tk.Tk):
    def __init__(self, words):
        super().__init__()
        self.words = words
        self.current_word = None
        self.correct_answers = 0
        self.incorrect_answers = 0

        # Создаем интерфейс
        self.title("Тренер слов")
        self.geometry("800x600")  # Устанавливаем размер окна
        self.configure(bg="#f0f0f0")  # Устанавливаем цвет фона
        self.word_frame = tk.Frame(self, bg="#f0f0f0", width=800, height=400)  # Устанавливаем размеры рамки
        self.word_frame.pack(pady=50)  # Добавляем отступы для рамки
        self.statistics_label = tk.Label(self, text="Правильные: 0, Неправильные: 0", bg="#f0f0f0", font=("Arial", 12))
        self.statistics_label.pack(side="bottom", pady=10)
        self.known_button = tk.Button(self, text="Знал", command=self.word_known, bg="#008000", fg="#ffffff", font=("Arial", 14))
        self.known_button.pack(side="left", padx=10, pady=10)  # Размещаем кнопку "Знал" слева
        self.not_known_button = tk.Button(self, text="Не знал", command=self.word_not_known, bg="#ff0000", fg="#ffffff", font=("Arial", 14))
        self.not_known_button.pack(side="right", padx=10, pady=10)  # Размещаем кнопку "Не знал" справа

        # Инициализируем проигрыватель музыки
        pygame.mixer.init()
        pygame.mixer.music.load("background_music.mp3")
        pygame.mixer.music.play(-1)  # Зацикливаем воспроизведение музыки

        # Показываем первое слово
        self.show_next_word()

    # Метод для показа следующего слова
    def show_next_word(self):
        if self.current_word:
            self.current_word.destroy()

        if self.words:  # Проверяем, есть ли слова в списке
            word, translation = random.choice(self.words)
            self.current_word = WordCard(self.word_frame, word, translation, self)
            self.current_word.pack(expand=True, fill="both")
        else:
            self.statistics_label.config(text="Вы изучили все слова!")

    # Метод для обработки ответа "Знал"
    def word_known(self):
        if self.current_word:
            self.correct_answers += 1
            self.update_statistics()
            word = self.current_word.word
            self.words = [w for w in self.words if w[0] != word]  # Удаляем слово из списка
            self.show_next_word()  # Отображаем следующее слово

    # Метод для обработки ответа "Не знал"
    def word_not_known(self):
        if self.current_word:
            self.incorrect_answers += 1
            self.update_statistics()
            self.show_next_word()  # Отображаем следующее слово

    # Метод для обновления статистики
    def update_statistics(self):
        self.statistics_label.config(text=f"Правильные: {self.correct_answers}, Неправильные: {self.incorrect_answers}")

# Загружаем слова из файла
words = read_words("words.txt")

# Создаем и запускаем приложение
app = WordTrainerApp(words)
app.mainloop()

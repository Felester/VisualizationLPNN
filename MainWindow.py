class MainWindow():
    from tkinter import Label, Button, Tk, Canvas, Text, WORD, LabelFrame, Entry, END
    from tkinter.ttk import Combobox
    from tkinter import messagebox as mb
    from tkinter import filedialog as fd
    from os import path

    import dataSettingsNN as ds
    import threading

    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.window = self.Tk()
        self.window.title(title)                                #Подпись
        self.window.geometry(str(width) + 'x' + str(height))    #Размер окна
        self.signature_font = ("Comic Sans MS", 10, "bold")


    def startForm(self):
        self.arrange_controls()
        self.start_value_entry()

        self.window.mainloop()



    def change_combo_box(self, event):
        print("New Element Selected")


    def open_data_file(self):
        initialdir = self.path.expanduser(u'~/Data'),
        file_name = self.fd.askopenfilename(initialdir=initialdir)
        self.entry_data_set.delete(0, self.END)
        self.entry_data_set.insert(0, file_name)


    def save_configuration(self):
        ansv, log_validation = self.ds.data_validation(self.entry_NNstruct.get(),
                                       self.entry_NNseed.get(),
                                       self.entry_zero_connection_seed.get(),
                                       self.entry_data_set.get())

        if log_validation != "":
            self.mb.showerror("Ошибка сохранения", log_validation)
        else:
            self.mb.showerror("Всё отлично", "Ошибок нет =)")


        #self.text.insert(1.0, log_validation)  # Добавление текста
        #print(ansv)
        print("Сохраняем")


    def arrange_controls(self):
        f_top = self.LabelFrame(self.window, text="Здесь будет рисоваться график", font=self.signature_font)
        self.c = self.Canvas(f_top, width=600, height=200, bg='white').place(relwidth=1, relheight = 1)
        f_top.place(relwidth=0.98, relheight=0.6, relx=0.01)

        # Панель конфигураций НС
        f_bot_1 = self.LabelFrame(self.window, text="Конфигурация НС", font=self.signature_font)
        self.combo_box = self.Combobox(f_bot_1)
        self.combo_box['values'] = ("Нейронная сеть №1", "Нейронная сеть №2")
        self.combo_box.current(0)  # вариант по умолчанию
        self.combo_box.bind("<<ComboboxSelected>>", self.change_combo_box)
        self.combo_box.place(relwidth=0.98, relheight=0.09, relx=0.01, rely=0.01)

        self.Label(f_bot_1, text="Структура НС в формате (10 5):").place(relwidth=0.98, relheight=0.1,
                                                                         relx=0.01, rely=0.11)

        self.entry_NNstruct = self.Entry(f_bot_1, bg="white")
        self.entry_NNstruct.place(relwidth=0.98, relheight=0.09, relx=0.01, rely=0.21)

        self.Label(f_bot_1, text="Сид рандома НС(целое число)").place(relwidth=0.98, relheight=0.09,
                                                                      relx=0.01, rely=0.31)

        self.entry_NNseed = self.Entry(f_bot_1, bg="white")
        self.entry_NNseed.place(relwidth=0.98, relheight=0.09, relx=0.01, rely=0.41)

        self.Label(f_bot_1, text="Сид рандома для обнуления связей").place(relwidth=0.98, relheight=0.09,
                                                                           relx=0.01, rely=0.51)

        self.entry_zero_connection_seed = self.Entry(f_bot_1, bg="white")
        self.entry_zero_connection_seed.place(relwidth=0.98, relheight=0.09, relx=0.01, rely=0.61)

        self.Label(f_bot_1, text="Файл с данными для обучения").place(relwidth=0.98, relheight=0.09,
                                                                      relx=0.01, rely=0.70)

        self.entry_data_set = self.Entry(f_bot_1, bg="white")
        self.entry_data_set.place(relwidth=0.6, relheight=0.08, relx=0.01, rely=0.81)
        self.Button(f_bot_1, text="Выбрать", command=self.open_data_file).place(relwidth=0.35, relheight=0.09,
                                                                                relx=0.63, rely=0.80)

        self.Button(f_bot_1, text="Сохранить", command=self.save_configuration).place(relwidth=0.48, relheight=0.09,
                                                                                      relx=0.51, rely=0.90)
        # Конец окна конфигурации НС
        f_bot_1.place(relwidth=0.38, relheight=0.39, relx=0.01, rely=0.6)

        # Панель управления
        f_bot_2 = self.LabelFrame(self.window, text="Панель управления", font=self.signature_font)

        self.Button(f_bot_2, text="Запустить обучение 1-ой НС", state='disabled',
                    command=self.open_data_file).place(relwidth=0.98, relheight=0.09, relx=0.01, rely=0.01)

        self.label_1st_network_learning_process = self.Label(f_bot_2, text="0 циклов обучения")
        self.label_1st_network_learning_process.place(relwidth=0.98, relheight=0.09,
                                                      relx=0.01, rely=0.11)

        self.Button(f_bot_2, text="Запустить обучение 2-ой НС", state='disabled',
                    command=self.open_data_file).place(relwidth=0.98, relheight=0.09, relx=0.01, rely=0.21)

        self.label_2st_network_learning_process = self.Label(f_bot_2, text="0 циклов обучения")
        self.label_2st_network_learning_process.place(relwidth=0.98, relheight=0.09,
                                                      relx=0.01, rely=0.31)

        self.Button(f_bot_2, text="Проанализировать результаты", state='disabled',
                    command=self.open_data_file).place(relwidth=0.98, relheight=0.09, relx=0.01, rely=0.41)

        self.Button(f_bot_2, text="Сохранить изображение", state='disabled',
                    command=self.open_data_file).place(relwidth=0.98, relheight=0.09, relx=0.01, rely=0.51)

        # Конец панели управления
        f_bot_2.place(relwidth=0.3, relheight=0.39, relx=0.4, rely=0.6)

        # Лог:
        f_bot_3 = self.LabelFrame(self.window, text="Лог программы:", font=self.signature_font)
        self.text = self.Text(f_bot_3, bg="white", fg='black', wrap=self.WORD)
        # scroll = self.Scrollbar(f_bot_3, command=self.text.yview, orient=self.VERTICAL)
        # scroll.pack(side=self.RIGHT, fill=self.Y)
        # self.text.config(yscrollcommand=scroll.set)
        self.text.place(relwidth=0.98, relheight=0.98, relx=0.01, rely=0.01)
        f_bot_3.place(relwidth=0.28, relheight=0.38, relx=0.71, rely=0.6)



    def start_value_entry(self):
        self.text.insert(1.0, "Программа запущена. \n")    #Добавление текста
        self.text.insert(1.0, "Интерфейс отрисован.\n")  # Добавление текста

        self.entry_NNstruct.insert(0, "15 5")
        self.entry_NNseed.insert(0, "1")
        self.entry_zero_connection_seed.insert(0, "1")
        self.entry_data_set.insert(0, "D:/Study/Python/THI/VisualizationLPNN/Data/data_1.data")


    def createButton(self):
        #self.text = self.Text(width=120, height=10, bg="white", fg='black', wrap=self.WORD)
        #self.text.place(x=10, y=440)

        #self.text.insert(1.0, "Процесс работы программы:\n")

        self.is_run = False

        #b1 = self.Button(text="Обучить НС", command=lambda: self.is_run or
                                             #self.threading.Thread(target=self.start_nn_training).start()).place(x=420, y=50)

        #b2 = self.Button(text="stop", command=self.stop_nn_training).place(x=420, y=80)

        #b3 = self.Button(text="ПРоверим на реальных данных!", command=self.load_picture_in_nn).place(x=420, y=110)



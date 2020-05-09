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
        self.settingsNN = []


    def start_form(self):
        self.arrange_controls()     # Панели, кнопки, поля для ввода
        self.set_default_settings()    #

        self.window.mainloop()


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
        f_bot_1.place(relwidth=0.30, relheight=0.39, relx=0.01, rely=0.6)

        # Панель управления
        f_bot_2 = self.LabelFrame(self.window, text="Панель управления", font=self.signature_font)

        self.Button(f_bot_2, text="Запустить обучение 1-ой НС", state='disabled',
                    command=self.open_data_file).place(relwidth=0.70, relheight=0.09, relx=0.01, rely=0.01)

        self.Button(f_bot_2, text="Стоп", state='disabled',
                    command=self.open_data_file).place(relwidth=0.27, relheight=0.09, relx=0.72, rely=0.01)

        self.label_1st_network_learning_process = self.Label(f_bot_2, text="0 циклов обучения")
        self.label_1st_network_learning_process.place(relwidth=0.98, relheight=0.09,
                                                      relx=0.01, rely=0.11)

        self.Button(f_bot_2, text="Запустить обучение 2-ой НС", state='disabled',
                    command=self.open_data_file).place(relwidth=0.70, relheight=0.09, relx=0.01, rely=0.21)

        self.Button(f_bot_2, text="Стоп", state='disabled',
                    command=self.open_data_file).place(relwidth=0.27, relheight=0.09, relx=0.72, rely=0.21)

        self.label_2st_network_learning_process = self.Label(f_bot_2, text="0 циклов обучения")
        self.label_2st_network_learning_process.place(relwidth=0.98, relheight=0.09,
                                                      relx=0.01, rely=0.31)

        self.Button(f_bot_2, text="Проанализировать результаты", state='disabled',
                    command=self.open_data_file).place(relwidth=0.98, relheight=0.09, relx=0.01, rely=0.41)

        self.Button(f_bot_2, text="Сохранить изображение", state='disabled',
                    command=self.open_data_file).place(relwidth=0.98, relheight=0.09, relx=0.01, rely=0.51)

        # Конец панели управленияы
        f_bot_2.place(relwidth=0.38, relheight=0.39, relx=0.32, rely=0.6)

        # Лог:
        f_bot_3 = self.LabelFrame(self.window, text="Лог программы:", font=self.signature_font)
        self.text = self.Text(f_bot_3, bg="white", fg='black', wrap=self.WORD)
        # scroll = self.Scrollbar(f_bot_3, command=self.text.yview, orient=self.VERTICAL)
        # scroll.pack(side=self.RIGHT, fill=self.Y)
        # self.text.config(yscrollcommand=scroll.set)
        self.text.place(relwidth=0.98, relheight=0.98, relx=0.01, rely=0.01)
        f_bot_3.place(relwidth=0.28, relheight=0.38, relx=0.71, rely=0.6)

        self.text.insert(1.0, "Интерфейс отрисован.\n")  # Добавление текста

    # Тут задаются стартовые настройки сетей
    def set_default_settings(self):
        self.add_setting_data("15", "1", "0", "D:/Study/Python/THI/VisualizationLPNN/Data/data_1.data")
        self.add_setting_data("16", "2", "1", "D:/Study/Python/THI/VisualizationLPNN/Data/data_1.data")
        self.show_network_settings(self.combo_box.current())
        self.text.insert(1.0, "Стартовые настройки были записаны \n")    #Добавление текста

    # При смене combo_box-а
    def change_combo_box(self, event):
        self.show_network_settings(self.combo_box.current())

    # Выбор файла с данными через проводник.
    def open_data_file(self):
        initialdir = self.path.expanduser(u'~/Data'),
        file_name = self.fd.askopenfilename(initialdir=initialdir)
        self.entry_data_set.delete(0, self.END)
        self.entry_data_set.insert(0, file_name)

    # Нужно координально переписывать
    def save_configuration(self):
        data_Setting, log_validation = self.ds.data_validation(self.entry_NNstruct.get(),
                                       self.entry_NNseed.get(),
                                       self.entry_zero_connection_seed.get(),
                                       self.entry_data_set.get())

        if log_validation != "":
            self.mb.showerror("Ошибка сохранения", log_validation)
        else:
            answer = self.mb.askyesno(title="Новые настройки", message="Применение данных настроек обнулит прогресс "
                                                                       "обучения НС. Применить новые настройки?")
            if answer:
                self.settingsNN[self.combo_box.current()] = self.ds.DataSetting(data_Setting)
                self.text.insert(1.0, "Новые параметры применены к НС №" + str(self.combo_box.current()+1) + " \n")  #

    # Эта функция сохраняет стартовые настройки.
    # В последствии они будут меняться на новые через поля ввода другой функцией
    def add_setting_data(self, NNstruct, NNseed, zero_connection_seed, way_data_set):
        data_Setting, log_validation = self.ds.data_validation(NNstruct,
                                       NNseed,
                                       zero_connection_seed,
                                       way_data_set)

        if log_validation != "":
            self.mb.showerror("Ошибка сохранения", log_validation)
        else:
            self.settingsNN.append(self.ds.DataSetting(data_Setting))
            self.text.insert(1.0, "Создана НС №" + str(len(self.settingsNN)) + " \n")  #

    def show_network_settings(self, index_combo_box):
        self.delete_show_settings()
        self.entry_NNstruct.insert(0, self.settingsNN[index_combo_box].get_NNstruct())
        self.entry_NNseed.insert(0, self.settingsNN[index_combo_box].get_NNseed())
        self.entry_zero_connection_seed.insert(0, self.settingsNN[index_combo_box].get_zero_connection_seed())
        self.entry_data_set.insert(0, self.settingsNN[index_combo_box].get_way_data_set())

    def delete_show_settings(self):
        self.entry_NNstruct.delete(0, self.END)
        self.entry_NNseed.delete(0, self.END)
        self.entry_zero_connection_seed.delete(0, self.END)
        self.entry_data_set.delete(0, self.END)

    # Буфер с кодом. Нужен будет в будущем
    def createButton(self):
        #self.text = self.Text(width=120, height=10, bg="white", fg='black', wrap=self.WORD)
        #self.text.place(x=10, y=440)

        #self.text.insert(1.0, "Процесс работы программы:\n")

        self.is_run = False

        #b1 = self.Button(text="Обучить НС", command=lambda: self.is_run or
                                             #self.threading.Thread(target=self.start_nn_training).start()).place(x=420, y=50)

        #b2 = self.Button(text="stop", command=self.stop_nn_training).place(x=420, y=80)

        #b3 = self.Button(text="ПРоверим на реальных данных!", command=self.load_picture_in_nn).place(x=420, y=110)



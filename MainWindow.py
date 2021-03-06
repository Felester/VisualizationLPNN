class MainWindow:
    from tkinter import Label, Button, Tk, Canvas, Text, WORD, LabelFrame, Entry, END, \
        NW, Scrollbar, HORIZONTAL, BOTTOM, X, LEFT, BOTH
    from tkinter.ttk import Combobox
    from tkinter import messagebox as mb
    from tkinter import filedialog as fd

    from os import path, getcwdb, getcwd
    import time

    import dataSettingsNN as ds
    import information_visualizer as iv

    import threading

    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.window = self.Tk()
        self.window.title(title)  # Подпись
        self.window.geometry(str(width) + 'x' + str(height))  # Размер окна
        self.signature_font = ("Comic Sans MS", 10, "bold")
        self.settingsNN = []
        self.analyzer = self.iv.InformationAnalyzer()

    def start_form(self):
        self.arrange_controls()  # Панели, кнопки, поля для ввода
        self.set_default_settings()  #
        self.redraw_canvas()
        self.window.mainloop()

    # Перерисовать график полностью, если изменился размер холста
    def redraw_canvas(self):
        canv_height = self.canvas.winfo_height()
        # Только если мы не рисуем и высота поменялась
        if (self.analyzer.get_drawing_process() == False) and (self.analyzer.get_canvas_height() != canv_height):
            self.analyzer.set_img_height(canv_height)
            image = self.analyzer.get_rendered_information(-1)
            self.canvas.create_image(5, 5, anchor=self.NW, image=image)
            self.canvas['scrollregion'] = (0, 0, self.analyzer.get_scrollregion_width(), 0)
            self.canvas.image = image

    def redraw_histogram(self, indexNN):
        if self.analyzer.get_possibility_render(indexNN) == True:
            image = self.analyzer.get_rendered_information(indexNN)
            self.canvas.create_image(5, 5, anchor=self.NW, image=image)
            self.canvas.image = image

    # Функция при закрытии окна, нужно закрывать потоки.
    def on_closing(self):
        print("Закрываем всё что есть")
        self.window.destroy()

    # Все поля, кнопки, метки, разметка и т.д.
    def arrange_controls(self):
        self.arr_info_label = []
        self.buttons_run_trainingNN = []
        self.buttons_stop_trainingNN = []
        self.combo_boxs_drawing_NN = []

        self.window.bind('<Configure>', lambda event: self.threading.Thread(target=self.redraw_canvas).start())
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())

        self.f_top = self.LabelFrame(self.window, text="Здесь будет рисоваться график", font=self.signature_font)
        self.canvas = self.Canvas(self.f_top, width=600, height=200, bg='white', scrollregion=(0, 0, 1500, 0))
        self.canvas.place(relwidth=1, relheight=1)
        hbar = self.Scrollbar(self.f_top, orient=self.HORIZONTAL)
        hbar.pack(side=self.BOTTOM, fill=self.X)
        hbar.config(command=self.canvas.xview)
        self.canvas.config(width=300, height=300)
        self.canvas.config(xscrollcommand=hbar.set)
        self.canvas.pack(side=self.LEFT, expand=True, fill=self.BOTH)
        self.f_top.place(relwidth=0.98, relheight=0.6, relx=0.01)

        # Панель конфигураций НС
        f_bot_1 = self.LabelFrame(self.window, text="Конфигурация НС", font=self.signature_font)
        self.combo_box = self.Combobox(f_bot_1)
        self.combo_box['values'] = ("Нейронная сеть №1", "Нейронная сеть №2")
        self.combo_box.current(0)  # вариант по умолчанию
        self.combo_box.bind("<<ComboboxSelected>>", self.change_combo_box_selection_network)
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

        self.Button(f_bot_1, text="Сменить БД", command=self.сhangeDB).place(relwidth=0.48, relheight=0.09,
                                                                                      relx=0.01, rely=0.90)

        self.Button(f_bot_1, text="Сохранить ИНС", command=self.save_configuration).place(relwidth=0.48, relheight=0.09,
                                                                                      relx=0.51, rely=0.90)
        # Конец окна конфигурации НС
        f_bot_1.place(relwidth=0.30, relheight=0.39, relx=0.01, rely=0.6)

        # Панель управления
        f_bot_2 = self.LabelFrame(self.window, text="Панель управления", font=self.signature_font)

        self.buttons_run_trainingNN.append(self.Button(f_bot_2, text="Запустить обучение 1-ой НС", state='disabled',
                                                       command=lambda: self.threading.Thread(
                                                           target=lambda: self.run_training(0)).start()))
        self.buttons_run_trainingNN[-1].place(relwidth=0.70, relheight=0.09, relx=0.01, rely=0.01)

        self.buttons_stop_trainingNN.append(self.Button(f_bot_2, text="Стоп", state='disabled',
                                                        command=lambda: self.stop_training(0)))
        self.buttons_stop_trainingNN[-1].place(relwidth=0.27, relheight=0.09, relx=0.72, rely=0.01)

        self.arr_info_label.append(self.Label(f_bot_2, text="0 циклов обучения"))
        self.arr_info_label[-1].place(relwidth=0.98, relheight=0.09, relx=0.01, rely=0.11)

        self.buttons_run_trainingNN.append(self.Button(f_bot_2, text="Запустить обучение 2-ой НС", state='disabled',
                                                       command=lambda: self.threading.Thread(
                                                           target=lambda: self.run_training(1)).start()))
        self.buttons_run_trainingNN[-1].place(relwidth=0.70, relheight=0.09, relx=0.01, rely=0.21)

        self.buttons_stop_trainingNN.append(self.Button(f_bot_2, text="Стоп", state='disabled',
                                                        command=lambda: self.stop_training(1)))
        self.buttons_stop_trainingNN[-1].place(relwidth=0.27, relheight=0.09, relx=0.72, rely=0.21)

        self.arr_info_label.append(self.Label(f_bot_2, text="0 циклов обучения"))
        self.arr_info_label[-1].place(relwidth=0.98, relheight=0.09, relx=0.01, rely=0.31)

        self.Label(f_bot_2, text="Задержка, секунд:").place(relwidth=0.48, relheight=0.09, relx=0.01, rely=0.41)
        self.Label(f_bot_2, text="Циклов обучения:").place(relwidth=0.48, relheight=0.09, relx=0.51, rely=0.41)

        self.entry_learning_delay = self.Entry(f_bot_2, bg="white")
        self.entry_learning_delay.place(relwidth=0.48, relheight=0.09, relx=0.01, rely=0.51)

        self.entry_training_cycles = self.Entry(f_bot_2, bg="white")
        self.entry_training_cycles.place(relwidth=0.48, relheight=0.09, relx=0.51, rely=0.51)

        self.Label(f_bot_2, text="Какие нейроны рисовать?").place(relwidth=0.98, relheight=0.09, relx=0.01, rely=0.61)
        #lambda event: self.threading.Thread(target=self.redraw_canvas).start()
        self.combo_boxs_drawing_NN.append(self.Combobox(f_bot_2))
        self.combo_boxs_drawing_NN[-1]['values'] = ("0 нейрон", "1 нейрон")
        self.combo_boxs_drawing_NN[-1].current(0)  # вариант по умолчанию
        self.combo_boxs_drawing_NN[-1].bind("<<ComboboxSelected>>", lambda event: self.change_combo_box_selection_neuron(0))
        self.combo_boxs_drawing_NN[-1].place(relwidth=0.48, relheight=0.09, relx=0.01, rely=0.71)

        self.combo_boxs_drawing_NN.append(self.Combobox(f_bot_2))
        self.combo_boxs_drawing_NN[-1]['values'] = ("0 нейрон", "1 нейрон")
        self.combo_boxs_drawing_NN[-1].current(0)  # вариант по умолчанию
        self.combo_boxs_drawing_NN[-1].bind("<<ComboboxSelected>>", lambda event: self.change_combo_box_selection_neuron(1))
        self.combo_boxs_drawing_NN[-1].place(relwidth=0.48, relheight=0.09, relx=0.51, rely=0.71)

        self.Button(f_bot_2, text="Проанализировать результаты",
                    command=self.analyze_results).place(relwidth=0.98, relheight=0.09, relx=0.01, rely=0.80)

        self.Button(f_bot_2, text="Сохранить изображение",
                    command=self.save_image).place(relwidth=0.98, relheight=0.09, relx=0.01, rely=0.90)
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

    def analyze_results(self):
        self.analyzer.find_similar()

        if self.analyzer.get_drawing_process() == False:
            image = self.analyzer.find_similar()

            self.canvas.create_image(5, 5, anchor=self.NW, image=image)
            self.canvas.image = image

    def сhangeDB(self):
        log_validation, data_setting = self.ds.DB_validation(self.entry_data_set.get())

        if log_validation != "":
            self.mb.showerror("Ошибка сохранения", log_validation)
        else:
            self.settingsNN[self.combo_box.current()].changeDB(data_setting)
            self.text.insert(1.0, "БД была изменена у ИНС №" + str(self.combo_box.current() + 1) + " \n")  #

    def save_image(self):
        img_name = str(self.settingsNN[0].get_training_cycle()) + '_' + str(self.settingsNN[1].get_training_cycle())
        self.analyzer.save_result_in_img(img_name)

    # Данный метод открывается в отдельном потоке для обучения НС.
    def run_training(self, indexNN):
        deley = 0
        training_cycles = 20000
        try:
            deley = float(self.entry_learning_delay.get().replace(',', '.'))
        except:
            self.mb.showerror("Ошибка данных", "Задержка обучения введена не корректно, "
                                               "будет использовано значение по умолчанию: 0")

        try:
            training_cycles = int(self.entry_training_cycles.get())
        except:
            self.mb.showerror("Ошибка данных", "Кол-во циклов обучения введено не корректно, "
                                               "будет использовано значение по умолчанию: " + str(training_cycles))
        end_training_cycles = training_cycles + self.settingsNN[indexNN].get_training_cycle()
        self.entry_NNstruct.get()

        self.text.insert(1.0, "Начали обучение НС №" + str(indexNN + 1) + " \n")  # Добавление текста
        self.settingsNN[indexNN].run_training()

        self.buttons_stop_trainingNN[indexNN]['state'] = 'normal'
        self.buttons_run_trainingNN[indexNN]['state'] = 'disabled'

        while self.settingsNN[indexNN].get_is_run() and end_training_cycles > self.settingsNN[
            indexNN].get_training_cycle():
            self.settingsNN[indexNN].training_cycle()
            self.arr_info_label[indexNN]['text'] = str(self.settingsNN[indexNN].get_training_cycle()) + " цикл обучения"

            self.analyzer.update_synapses(self.settingsNN[indexNN].get_synapse_values(), indexNN)

            #self.threading.Thread(target=lambda: self.redraw_histogram(indexNN)).start()

            self.redraw_histogram(indexNN)

            self.time.sleep(deley)
        if self.settingsNN[indexNN].get_is_run():
            self.stop_training(indexNN)

    # Заполняем комбобоксы на основе размера сетей
    def fill_selection_neuron(self, indexNN):
        number = self.settingsNN[indexNN].get_number_of_network_neurons()
        valuesCombobox = []
        for i in range(number):
            valuesCombobox.append("Нейрон " + str(i))
        if number > 1:
            valuesCombobox.append("Все нейроны")

        valuesCombobox.append("Не рисовать")
        self.combo_boxs_drawing_NN[indexNN]["values"] = valuesCombobox

    def stop_training(self, indexNN):
        self.settingsNN[indexNN].stop_training()

        self.buttons_run_trainingNN[indexNN]['state'] = 'normal'
        self.buttons_stop_trainingNN[indexNN]['state'] = 'disabled'

        self.text.insert(1.0, "Точность НС № " + str(indexNN + 1) + " = " +
                         self.settingsNN[indexNN].get_accuracy_NN() + " \n")  # Добавление текста
        self.text.insert(1.0, "Закончили обучение НС № " + str(indexNN + 1) + " \n")  # Добавление текста

    # Тут задаются стартовые настройки сетей
    def set_default_settings(self):
        self.add_setting_data("10", "1", "0", self.getcwd() + "\Data\data_1.data")
        self.add_setting_data("16", "2", "1", self.getcwd() + "\Data\data_1.data")

        self.analyzer.update_synapses(self.settingsNN[0].get_synapse_values(), 0)
        self.analyzer.update_synapses(self.settingsNN[1].get_synapse_values(), 1)

        # Комбобоксы и активация кнопок
        self.fill_selection_neuron(0)
        self.fill_selection_neuron(1)
        self.buttons_run_trainingNN[0]['state'] = 'normal'
        self.buttons_run_trainingNN[1]['state'] = 'normal'

        self.show_network_settings(self.combo_box.current())
        self.text.insert(1.0, "Стартовые настройки были записаны \n")  # Добавление текста

    # При смене combo_box-ов с выбором нейронов
    def change_combo_box_selection_neuron(self, index):
        lon = self.analyzer.set_imaged_neuron(self.combo_boxs_drawing_NN[index].current(), index)
        self.redraw_histogram(index)
        self.text.insert(1.0, lon)

    # При смене combo_box-а с настройками ИНС
    def change_combo_box_selection_network(self, event):
        self.show_network_settings(self.combo_box.current())

    # Выбор файла с данными через проводник.
    def open_data_file(self):
        initialdir = self.path.expanduser(u'~/Data'),
        file_name = self.fd.askopenfilename(initialdir=initialdir)
        self.entry_data_set.delete(0, self.END)
        self.entry_data_set.insert(0, file_name)

    # Нужна смена параметров
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
                self.analyzer.update_synapses(self.settingsNN[self.combo_box.current()].get_synapse_values(), self.combo_box.current())
                self.redraw_histogram(self.combo_box.current())
                self.text.insert(1.0, "Новые параметры применены к НС №" + str(self.combo_box.current() + 1) + " \n")  #

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

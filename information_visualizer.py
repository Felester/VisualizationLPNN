
class InformationAnalyzer:
    from PIL import Image, ImageDraw, ImageTk, ImageFont
    import affinity_search_engine as ASE
    color_histogram = [(0, 0, 255), (0, 250, 0)]

    def __init__(self):
        self._synapse_values = [[], []]
        self._img_histograms = [[], []]
        self._index_neuron = [0, 0]

        self._widthLine = 1
        self._drawing_process = False

        self._width_histogram = 10      # Ширина 1-ой гистограммы
        self._histogram_spacing = 30    # Между гистограммами

        self._image_width = 0           # Стартовая ширина изображения(меняется, когда структура сетей меняется/задаётся)

        self.Xoffset = 20   # Общее смещение всего(включая осей)
        self.X_start_schedule = [10]      # Дополнительное смещение для гистограммы(кроме осей)
        self.X_start_schedule.append(self._width_histogram + self.X_start_schedule[-1])

        self.set_img_height(500)    # Координаты для осей на основе высоты

    # Вычисляет схожесть нейронов
    def find_similar(self):
        cla_top_similar = self.ASE.affinity_analyzer(self._synapse_values, self._index_neuron)
        top_similar = cla_top_similar.get_top_similar()

        return self._rendered_similar(top_similar)

    def _rendered_similar(self, top_similar_str):
        self._drawing_process = True
        histogram_shift = self.Xoffset + self.X_start_schedule[0]

        font = self.ImageFont.truetype("19168.ttf", 16)
        image = self.Image.alpha_composite(self._img_histograms[0], self.ImageBlank)
        image = self.Image.alpha_composite(self._img_histograms[1], image)

        y_shift = 0
        draw = self.ImageDraw.Draw(image)

        for j in range(len(top_similar_str)):
            draw.text((histogram_shift, self.cur_y_2 + y_shift), top_similar_str[j], self.color_histogram[j//2], font=font)
            y_shift += 20
        del draw

        image = self.ImageTk.PhotoImage(image)
        self._drawing_process = False
        return image




    # Смена индекса нейрона, который будет визуализирован
    def set_imaged_neuron(self, index_neuron, index_network):
        self._index_neuron[index_network] = index_neuron
        self._get_rendered_histogram(index_network)
        print(len(self._synapse_values[index_network][0]))
        if index_neuron < len(self._synapse_values[index_network][0]):
            log = "Поменяли отображаемый нейрон ИНС № " + str(index_network+1) + " на " + str(index_neuron) + " \n"
        elif index_neuron == len(self._synapse_values[index_network][0]):
            log = "Поменяли отображаемый нейрон ИНС № " + str(index_network + 1) + " на <ВСЕ> \n"
        else:
            log = "Отрисовка ИНС № " + str(index_network + 1) + " остановлена \n"

        return log

    def get_canvas_height(self):
        return self.canvas_height

    def get_scrollregion_width(self):
        return self._image_width

    def _update_size_image(self):
        self._image_width = self._get_size_image()
        self.ImageBlank = self._draw_starting_canvas()

    # Ширина изображения на основе размера нейронной сети
    def _get_size_image(self):
        #if len(self._synapse_values[0]) > 0 and len(self._synapse_values[1]) > 0:
            #if len(self._synapse_values[0]):
                #return len(self._synapse_values[0][0]) * len(self._synapse_values[0]) * self._histogram_spacing + 100
            #else:
                #return len(self._synapse_values[1][0]) * len(self._synapse_values[1]) * self._histogram_spacing + 100
        #else:
            return 2500

    # Рисует ли щас хоть 1 поток?
    def get_drawing_process(self):
        return self._drawing_process

    # Запись новых значений синапсов
    def update_synapses(self, synapse_values, network_index):
        self._synapse_values[network_index] = synapse_values
        if self._get_size_image() != self._image_width:
            self._update_size_image()

    def set_img_height(self, height):
        # График строится в этом промежутке
        self.canvas_height = height
        self.cur_y_1 = self.canvas_height * 0.1
        self.axis_height = self.canvas_height * 0.4
        self.cur_y_2 = self.canvas_height * 0.7

        # Высота гистограммы в пикселях
        self.height_histogram = self.axis_height - self.cur_y_1
        self.ImageBlank = self._draw_starting_canvas()
        self._update_size_image()

    # Рисование гистограмм на заготовке
    def get_rendered_information(self, indexNN):
        self._drawing_process = True
        #image = self.ImageBlank.copy()

        if indexNN >= 0:
            self._get_rendered_histogram(indexNN)
        elif indexNN == -1:
            self._get_rendered_histogram(0)
            self._get_rendered_histogram(1)


        image = self.Image.alpha_composite(self._img_histograms[0], self.ImageBlank)
        image = self.Image.alpha_composite(self._img_histograms[1], image)

        image = self.ImageTk.PhotoImage(image)
        self._drawing_process = False
        return image

    # Перерисовать гистограмму с заданным индексом сети
    def _get_rendered_histogram(self, indexNN):
        image = self.Image.new("RGBA", (self._image_width + 50, self.canvas_height), (0, 0, 0, 0))
        draw = self.ImageDraw.Draw(image)

        if len(self._synapse_values[indexNN][0]) != 0:
            index_neuron = 0
            histogram_shift = self.Xoffset + self.X_start_schedule[indexNN] # + i * self._histogram_spacing

            transpose_matrix = list(map(list, zip(*self._synapse_values[indexNN])))


            if self._index_neuron[indexNN] == len(transpose_matrix):
                for neuron in transpose_matrix:
                    histogram_shift = self._rendered_histogram_1_neuron(indexNN, index_neuron,
                                                                        neuron,
                                                                        draw, histogram_shift)
                    index_neuron = index_neuron + 1
            elif self._index_neuron[indexNN] < len(transpose_matrix):
                histogram_shift = self._rendered_histogram_1_neuron(indexNN, self._index_neuron[indexNN],
                                                                    transpose_matrix[self._index_neuron[indexNN]],
                                                                    draw, histogram_shift)

        del draw
        if self._index_neuron[indexNN] <= len(transpose_matrix):
            self._img_histograms[indexNN] = image.copy()

    # добавляет к рисунку гистограммы с 1-го нейрона. Возможно можно запустить на GPU с небольшими поправками.
    def _rendered_histogram_1_neuron(self, index_network, index_neuron, neuron_matrix, draw, histogram_shift):
        font = self.ImageFont.truetype("19168.ttf", 16)
        if index_network == 0:
            draw.text((histogram_shift, 10), "Сеть - " + str(index_network + 1) + ", нейрон - " + str(index_neuron),
                      self.color_histogram[index_network], font=font)
        else:
            draw.text((histogram_shift + 150, 10), "Сеть - " + str(index_network + 1) + ", нейрон - " + str(index_neuron),
                      self.color_histogram[index_network], font=font)

        for synapse in neuron_matrix:
            draw.rectangle((histogram_shift, self.axis_height,
                            histogram_shift + self._width_histogram,
                            self.axis_height - self.height_histogram * synapse),
                           fill=self.color_histogram[index_network])
            histogram_shift += self._histogram_spacing
        # Между нейронами прямая линия
        if index_network == 0:
            draw.line(((histogram_shift + self._width_histogram - self._histogram_spacing / 2, self.cur_y_1),
                       (histogram_shift + self._width_histogram - self._histogram_spacing / 2, self.canvas_height)),
                      fill=(0, 0, 0), width=self._widthLine)

        return histogram_shift

    # Оси и подписи к ним
    def _draw_starting_canvas(self):
        self._drawing_process = True
        image = self.Image.new("RGBA", (self._image_width+50, self.canvas_height), (0, 0, 0, 0))

        draw = self.ImageDraw.Draw(image)

        draw.line(((0, 0), (self._image_width, 0)), fill=(0, 0, 255), width=self._widthLine)
        draw.line(((0, 0), (0, self.canvas_height)), fill=(0, 0, 255), width=self._widthLine)
        draw.line(((self._image_width, self.canvas_height), (0, self.canvas_height)), fill=(0, 0, 255),
                  width=self._widthLine)
        draw.line(((self._image_width, self.canvas_height), (self._image_width, 0)), fill=(0, 0, 255),
                  width=self._widthLine)


        # Ось X
        draw.line(((self.Xoffset, self.axis_height), (self._image_width + 150, self.axis_height)),
                  fill=(0, 0, 0), width=self._widthLine)
        # Ось Y
        draw.line(
            ((self.Xoffset, self.cur_y_1 - self.axis_height * 0.1),
             (self.Xoffset, self.canvas_height)), fill=(0, 0, 0), width=self._widthLine)

        # Подписи осей
        draw.text((self.Xoffset - 10, self.axis_height - 5), '0', (0, 0, 0))
        draw.text((self.Xoffset - 10, self.cur_y_1 - 5), '1', (0, 0, 0))
        draw.text((self.Xoffset - 15, self.cur_y_2 - 5), '-1', (0, 0, 0))

        for x in range(self.Xoffset, self._image_width, 4):
            draw.line([(x, self.cur_y_1), (x + 2, self.cur_y_1)], fill=(170, 170, 170))
            draw.line([(x, self.cur_y_2), (x + 2, self.cur_y_2)], fill=(170, 170, 170))

        del draw
        self._drawing_process = False
        return image




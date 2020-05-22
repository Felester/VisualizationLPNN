
class InformationAnalyzer:
    from PIL import Image, ImageDraw, ImageTk
    color_histogram = [(0, 0, 255), (0, 255, 0)]

    def __init__(self):
        self._synapse_values = [[], []]
        self._img_histograms = [[], []]
        self._widthLine = 1
        self._drawing_process = False

        self._width_histogram = 10      # Ширина 1-ой гистограммы
        self._histogram_spacing = 30    # Между гистограммами

        self._image_width = 0           # Стартовая ширина изображения(меняется, когда структура сетей меняется/задаётся)

        self.Xoffset = 20   # Общее смещение всего(включая осей)
        self.X_start_schedule = [10]      # Дополнительное смещение для гистограммы(кроме осей)
        self.X_start_schedule.append(self._width_histogram + self.X_start_schedule[-1])

        self.set_img_height(500)    # Координаты для осей на основе высоты

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
            return 100

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
            i = 0
            histogram_shift = self.Xoffset + self.X_start_schedule[indexNN] + i * self._histogram_spacing

            transpose_matrix = list(map(list, zip(*self._synapse_values[indexNN])))
            for neuron in transpose_matrix:
                for synapse in neuron:
                    draw.rectangle((histogram_shift, self.axis_height,
                                    histogram_shift + self._width_histogram,
                                    self.axis_height - self.height_histogram * synapse),
                                   fill=self.color_histogram[indexNN])
                    histogram_shift += self._histogram_spacing

                # Между нейронами прямая линия
                if indexNN ==0:
                    draw.line(((histogram_shift + self._width_histogram - self._histogram_spacing / 2, self.cur_y_1),
                           (histogram_shift + self._width_histogram - self._histogram_spacing / 2, self.canvas_height)),
                          fill=(0, 0, 0), width=self._widthLine)

        del draw
        self._img_histograms[indexNN] = image.copy()

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




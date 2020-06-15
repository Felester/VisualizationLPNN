
class Drawer:
    from PIL import Image, ImageDraw, ImageTk, ImageFont
    _color_histogram = [(0, 0, 255), (0, 250, 0)]
    _font = ImageFont.truetype("19168.ttf", 16)
    def __init__(self, height = 600, width = 800):
        self._img_histograms = [[], []]
        self._widthLine = 1
        self._width_histogram = 10              # Ширина 1-ой гистограммы
        self._histogram_spacing = 30            # Между гистограммами
        self._image_width = width               # Стартовая ширина изображения(меняется, когда структура сетей меняется/задаётся)
        self._X_offset = 20                     # Общее смещение всего(включая осей)
        self._X_start_schedule = [10]           # Дополнительное смещение для гистограммы(каждой отдельно)
        self._X_start_schedule.append(self._width_histogram + self._X_start_schedule[-1])

        self.set_img_height(height)             # Координаты для осей на основе высоты

    # Поменять/задать координаты для диапазона гистограмм
    def set_img_height(self, height):
        # График строится в этом промежутке
        self._canvas_height = height
        self._cur_y_1 = self._canvas_height * 0.1
        self._axis_height = self._canvas_height * 0.4
        self._cur_y_2 = self._canvas_height * 0.7

        # Высота гистограммы в пикселях
        self._height_histogram = self._axis_height - self._cur_y_1
        self._image_blank = self._draw_starting_canvas()
        self.update_size_image()

    def get_canvas_height(self):
        return self._canvas_height

    def get_scrollregion_width(self):
        return self._image_width

    # Ширина изображения на основе размера нейронной сети
    def get_size_image(self):
        #if len(self._synapse_values[0]) > 0 and len(self._synapse_values[1]) > 0:
            #if len(self._synapse_values[0]):
                #return len(self._synapse_values[0][0]) * len(self._synapse_values[0]) * self._histogram_spacing + 100
            #else:
                #return len(self._synapse_values[1][0]) * len(self._synapse_values[1]) * self._histogram_spacing + 100
        #else:
            return 2500

    # Вычислить ширину изображения и отрисовать заготовку(оси, подписи)
    def update_size_image(self):
        self._image_width = self.get_size_image()
        self._image_blank = self._draw_starting_canvas()

    # Оси и подписи к ним
    def _draw_starting_canvas(self):
        image = self.Image.new("RGBA", (self._image_width+50, self._canvas_height), (0, 0, 0, 0))

        draw = self.ImageDraw.Draw(image)

        draw.line(((0, 0), (self._image_width, 0)), fill=(0, 0, 255), width=self._widthLine)
        draw.line(((0, 0), (0, self._canvas_height)), fill=(0, 0, 255), width=self._widthLine)
        draw.line(((self._image_width, self._canvas_height), (0, self._canvas_height)), fill=(0, 0, 255),
                  width=self._widthLine)
        draw.line(((self._image_width, self._canvas_height), (self._image_width, 0)), fill=(0, 0, 255),
                  width=self._widthLine)

        # Ось X
        draw.line(((self._X_offset, self._axis_height), (self._image_width + 150, self._axis_height)),
                  fill=(0, 0, 0), width=self._widthLine)
        # Ось Y
        draw.line(
            ((self._X_offset, self._cur_y_1 - self._axis_height * 0.1),
             (self._X_offset, self._canvas_height)), fill=(0, 0, 0), width=self._widthLine)

        # Подписи осей
        draw.text((self._X_offset - 10, self._axis_height - 5), '0', (0, 0, 0))
        draw.text((self._X_offset - 10, self._cur_y_1 - 5), '1', (0, 0, 0))
        draw.text((self._X_offset - 15, self._cur_y_2 - 5), '-1', (0, 0, 0))

        for x in range(self._X_offset, self._image_width, 4):
            draw.line([(x, self._cur_y_1), (x + 2, self._cur_y_1)], fill=(170, 170, 170))
            draw.line([(x, self._cur_y_2), (x + 2, self._cur_y_2)], fill=(170, 170, 170))

        del draw
        return image

    # добавляет к рисунку гистограммы с 1-го нейрона. Возможно можно запустить на GPU с небольшими поправками.
    def _rendered_histogram_1_neuron(self, index_network, index_neuron, neuron_matrix, draw, histogram_shift):
        if index_network == 0:
            draw.text((histogram_shift, 10), "Сеть - " + str(index_network + 1) + ", нейрон - " + str(index_neuron),
                      self._color_histogram[index_network], font=self._font)
        else:
            draw.text((histogram_shift + 150, 10), "Сеть - " + str(index_network + 1) + ", нейрон - " + str(index_neuron),
                      self._color_histogram[index_network], font=self._font)

        for synapse in neuron_matrix:
            draw.rectangle((histogram_shift, self._axis_height,
                            histogram_shift + self._width_histogram,
                            self._axis_height - self._height_histogram * synapse),
                           fill=self._color_histogram[index_network])
            histogram_shift += self._histogram_spacing
        # Между нейронами прямая линия
        if index_network == 0:
            draw.line(((histogram_shift + self._width_histogram - self._histogram_spacing / 2, self._cur_y_1),
                       (histogram_shift + self._width_histogram - self._histogram_spacing / 2, self._canvas_height)),
                      fill=(0, 0, 0), width=self._widthLine)

        return histogram_shift

    # Перерисовать гистограмму с заданным индексом сети
    def _rendered_histogram(self, index_network, neuron_indices_for_rendering, synapse_values):
        image = self.Image.new("RGBA", (self._image_width + 50, self._canvas_height), (0, 0, 0, 0))
        draw = self.ImageDraw.Draw(image)

        if len(synapse_values[index_network][0]) != 0:
            index_neuron = 0
            histogram_shift = self._X_offset + self._X_start_schedule[index_network] # + i * self._histogram_spacing

            transpose_matrix = list(map(list, zip(*synapse_values[index_network])))

            if neuron_indices_for_rendering[index_network] == len(transpose_matrix):
                for neuron in transpose_matrix:
                    histogram_shift = self._rendered_histogram_1_neuron(index_network, index_neuron,
                                                                        neuron,
                                                                        draw, histogram_shift)
                    index_neuron = index_neuron + 1
            elif neuron_indices_for_rendering[index_network] < len(transpose_matrix):
                histogram_shift = self._rendered_histogram_1_neuron(index_network, neuron_indices_for_rendering[index_network],
                                                                    transpose_matrix[neuron_indices_for_rendering[index_network]],
                                                                    draw, histogram_shift)

        del draw
        if neuron_indices_for_rendering[index_network] <= len(transpose_matrix):
            self._img_histograms[index_network] = image.copy()

    # Вернуть отрисованное изображение(В зависимости от index_network рисует всё или что то одно)
    def get_rendered_information(self, index_network, index_neuron, synapse_values):
        if index_network >= 0:
            self._rendered_histogram(index_network, index_neuron, synapse_values)
        elif index_network == -1:
            self._rendered_histogram(0, index_neuron, synapse_values)
            self._rendered_histogram(1, index_neuron, synapse_values)

        image = self.Image.alpha_composite(self._img_histograms[0], self._image_blank)
        image = self.Image.alpha_composite(self._img_histograms[1], image)

        image = self.ImageTk.PhotoImage(image)
        return image

    # Добавить к рисунку анализ схожести
    def rendered_similar(self, top_similar_str):
        histogram_shift = self._X_offset + self._X_start_schedule[0]

        image = self.Image.alpha_composite(self._img_histograms[0], self._image_blank)
        image = self.Image.alpha_composite(self._img_histograms[1], image)
        y_shift = 0

        draw = self.ImageDraw.Draw(image)
        for j in range(len(top_similar_str)):
            draw.text((histogram_shift, self._cur_y_2 + y_shift), top_similar_str[j], self._color_histogram[j // 2],
                      font=self._font)
            y_shift += 20
        del draw

        image = self.ImageTk.PhotoImage(image)
        return image

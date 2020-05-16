
class InformationAnalyzer:
    from PIL import Image, ImageDraw, ImageTk

    def __init__(self):
        self._synapse_values = [[], []]
        self._widthLine = 1
        self._width_histogram = 5      # Ширина 1-ой гистограммы
        self._histogram_spacing = 20    # Между гистограммами

        self._image_width = 0           # Стартовая ширина изображения(меняется, когда структура сетей меняется/задаётся)

        self.Xoffset = 20   # Общее смещение всего(включая осей)
        self.X_start_schedule = 10      # Дополнительное смещение для гистограммы(кроме осей)

        # График строится в этом промежутке
        self.canvas_height = 540
        self.cur_y_1 = self.canvas_height * 0.1
        self.axis_height = self.canvas_height * 0.4
        self.cur_y_2 = self.canvas_height * 0.7

        # Высота гистограммы в пикселях
        self.height_histogram = self.axis_height - self.cur_y_1
        self.ImageBlank = self._draw_starting_canvas()

    def get_scrollregion_width(self):
        return self._image_width

    def _update_size_image(self):
        self._image_width = self._get_size_image()
        self.ImageBlank = self._draw_starting_canvas()

    def _get_size_image(self):
        return 1000 #len(self._synapse_values[0][0]) * len(self._synapse_values[0]) * self._histogram_spacing + 100

    def update_synapses(self, synapse_values, network_index):
        self._synapse_values[network_index] = synapse_values
        if self._get_size_image() != self._image_width:
            self._update_size_image()

    def set_img_height(self, height):
        self.canvas_height = height
        self.cur_y_1 = self.canvas_height * 0.1
        self.axis_height = self.canvas_height * 0.4
        self.cur_y_2 = self.canvas_height * 0.7

        # Высота гистограммы в пикселях
        self.height_histogram = self.axis_height - self.cur_y_1
        self.ImageBlank = self._draw_starting_canvas()

    def get_rendered_information(self):
        image = self.ImageBlank.copy()
        draw = self.ImageDraw.Draw(image)

        if len(self._synapse_values[0][0]) != 0:
            i = 0
            histogram_shift = self.Xoffset + self.X_start_schedule + i*self._histogram_spacing + self.X_start_schedule

            transpose_matrix = list(map(list, zip(*self._synapse_values[0])))
            for neuron in transpose_matrix:
                for synapse in neuron:
                    draw.rectangle((histogram_shift, self.axis_height,
                                    histogram_shift+self._width_histogram,
                                    self.axis_height-self.height_histogram*synapse),
                                   fill=(0, 0, 255))
                    histogram_shift += self._histogram_spacing

                # Между нейронами прямая линия
                draw.line(((histogram_shift + self._width_histogram - self._histogram_spacing/2, self.cur_y_1),
                           (histogram_shift + self._width_histogram - self._histogram_spacing/2, self.canvas_height)),
                          fill=(0, 0, 0), width=self._widthLine)

        del draw

        image = self.ImageTk.PhotoImage(image)
        return image

    # Оси и подписи к ним
    def _draw_starting_canvas(self):
        image = self.Image.new("RGBA", (self._image_width+50, self.canvas_height), (0, 0, 0, 0))

        draw = self.ImageDraw.Draw(image)

        draw.line(((0, 0), (self._image_width, 0)), fill=(0, 0, 255), width=self._widthLine)
        draw.line(((0, 0), (0, self.canvas_height)), fill=(0, 0, 255), width=self._widthLine)
        draw.line(((self._image_width, self.canvas_height), (0, self.canvas_height)), fill=(0, 0, 255),
                  width=self._widthLine)
        draw.line(((self._image_width, self.canvas_height), (self._image_width, 0)), fill=(0, 0, 255),
                  width=self._widthLine)


        # Ось X
        draw.line(((self.Xoffset + self.X_start_schedule, self.axis_height), (self._image_width + 150, self.axis_height)),
                  fill=(0, 0, 0), width=self._widthLine)
        # Ось Y
        draw.line(
            ((self.Xoffset + self.X_start_schedule, self.cur_y_1 - self.axis_height * 0.1),
             (self.Xoffset + self.X_start_schedule, self.canvas_height)), fill=(0, 0, 0), width=self._widthLine)

        # Подписи осей
        draw.text((self.Xoffset + self.X_start_schedule - 10, self.axis_height - 5), '0', (0, 0, 0))
        draw.text((self.Xoffset + self.X_start_schedule - 10, self.cur_y_1 - 5), '1', (0, 0, 0))
        draw.text((self.Xoffset + self.X_start_schedule - 15, self.cur_y_2 - 5), '-1', (0, 0, 0))

        for x in range(self.Xoffset + self.X_start_schedule, self._image_width, 4):
            draw.line([(x, self.cur_y_1), (x + 2, self.cur_y_1)], fill=(170, 170, 170))
            draw.line([(x, self.cur_y_2), (x + 2, self.cur_y_2)], fill=(170, 170, 170))

        del draw
        return image




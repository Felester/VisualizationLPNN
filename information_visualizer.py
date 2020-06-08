
class InformationAnalyzer:
    import affinity_search_engine as ASE
    import drawing
    color_histogram = [(0, 0, 255), (0, 250, 0)]

    def __init__(self):
        self._drawer = self.drawing.Drawer()
        self._synapse_values = [[], []]
        self._img_histograms = [[], []]
        self._index_neuron = [0, 0]

        self._drawing_process = False
        self._image_width = 500           # Стартовая ширина изображения(меняется, когда структура сетей меняется/задаётся)

    # Вычисляет схожесть нейронов
    def find_similar(self):
        cla_top_similar = self.ASE.affinity_analyzer(self._synapse_values, self._index_neuron)
        top_similar = cla_top_similar.get_top_similar()
        return self._rendered_similar(top_similar)

    # Добавить к рисунку анализ схожести
    def _rendered_similar(self, top_similar_str):
        image = self._drawer.rendered_similar(top_similar_str)
        return image

    # Смена индекса нейрона, который будет визуализирован
    def set_imaged_neuron(self, index_neuron, index_network):
        self._index_neuron[index_network] = index_neuron
        self._drawer.get_rendered_histogram(index_network, self._index_neuron, self._synapse_values)

        if index_neuron < len(self._synapse_values[index_network][0]):
            log = "Поменяли отображаемый нейрон ИНС № " + str(index_network+1) + " на " + str(index_neuron) + " \n"
        elif index_neuron == len(self._synapse_values[index_network][0]):
            log = "Поменяли отображаемый нейрон ИНС № " + str(index_network + 1) + " на <ВСЕ> \n"
        else:
            log = "Отрисовка ИНС № " + str(index_network + 1) + " остановлена \n"
        return log


    # Всё что ниже-сквозная фигня, переписывать как только заработает, только как....
    def get_canvas_height(self):
        return self._drawer.get_canvas_height()

    def get_scrollregion_width(self):
        return self._drawer.get_scrollregion_width()

    def set_img_height(self, height):
        return self._drawer.set_img_height(height)

    # Рисует ли щас хоть 1 поток?
    def get_drawing_process(self):
        return self._drawing_process

    # Рисование гистограмм на заготовке
    def get_rendered_information(self, index_network):
        self._drawing_process = True
        image = self._drawer.get_rendered_information(index_network, self._index_neuron, self._synapse_values)
        self._drawing_process = False
        return image

    # Запись новых значений синапсов
    def update_synapses(self, synapse_values, network_index):
        self._synapse_values[network_index] = synapse_values
        if self._drawer.get_size_image() != self._image_width:
            self._drawer.update_size_image()

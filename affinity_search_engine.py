class affinity_analyzer:
    comparison_order = [[0, 0],
                        [0, 1],
                        [1, 0],
                        [1, 1]]

    def __init__(self, synapse_values, indices_elected_neuron):
        self._top_similar = [[] for i in range(len(self.comparison_order))]
        if len(synapse_values) > 0:
            self._find_top_similar(synapse_values, indices_elected_neuron)
        else:
            print("Инициализация объекта поиска похожих нейронов прошла с ошибкой.")

    # Находит ТОП схожих с заданными
    def _find_top_similar(self, synapse_values, indices_elected_neuron):
        lists_coincidence = []
        for i in range(len(self.comparison_order)):
            lists_coincidence.append(self._neuron_comparison(self.comparison_order[i][0], self.comparison_order[i][1],
                                                             indices_elected_neuron[i//2], synapse_values))

        for j in range(len(lists_coincidence)):
            for i in range(3):
                self._top_similar[j].append(
                    [lists_coincidence[j].index(min(lists_coincidence[j])), min(lists_coincidence[j])])
                lists_coincidence[j][self._top_similar[j][-1][0]] = 1000

    def update_synapse(self, synapse_values, indices_elected_neuron):
        if len(synapse_values) > 0:
            self._find_top_similar(synapse_values, indices_elected_neuron)
            return self._generate_string_response()
        else:
            print("Обновление данных объекта поиска похожих нейронов прошла с ошибкой.")

    # Получить строку с ТОП схожими нейронами
    def get_top_similar(self):
        return self._generate_string_response()

    # Сравнить указанный нейрон первой сети со всеми нейронами второй. Вернуть список сходства
    def _neuron_comparison(self, index_network_1, index_network_2, index_neuron, synapse_values):
        list_coincidence = []

        # По нейронам ИНС
        for i in range(len(synapse_values[index_network_2][index_neuron])):
            degree_of_coincidence = 0
            # По связям
            for j in range(len(synapse_values[index_network_2])):
                degree_of_coincidence += abs(synapse_values[index_network_1][j][index_neuron] -
                                             synapse_values[index_network_2][j][i])

            list_coincidence.append(degree_of_coincidence)
        return list_coincidence

    # Создаёт список для вывода на экран
    def _generate_string_response(self):
        top_similar_str = ["" for i in range(len(self._top_similar))]
        for j in range(len(self._top_similar)):
            top_similar_str[j] += "Самый похожий в сети " + str(self.comparison_order[j][1] + 1) + ": "
            for top in self._top_similar[j]:
                top_similar_str[j] += "Нейрон: " + str(top[0]) + " - отличия: " + str(round(top[1], 1)) + "; "
        return top_similar_str

import numpy as np


class NeuralNetwork:
    def __init__(self, seedRandom, NetworkStructure, zeroСonnection):
        # Чтобы контролировать рандом
        np.random.seed(seedRandom)
        self._arraySynapticScales = []

        # инициализируем веса случайным образом со средним 0
        for i in range(len(NetworkStructure)-1):
            self._arraySynapticScales.append(2 * np.random.random((NetworkStructure[i], NetworkStructure[i + 1])) - 1)

        #[Слой][нейрон][вес связи к какому нейрону]
        for zeros in zeroСonnection:
            self._arraySynapticScales[zeros[0]][zeros[1]][zeros[2]] = 0

    def get_array_synaptic_scales(self):
        return self._arraySynapticScales

    # Сигмоида
    @staticmethod
    def _nonlin(x, deriv=False):
        if(deriv==True):
            return x*(1-x)
        return 1/(1+np.exp(-x))

    # Мы обучаем нейронную сеть в процессе проб и ошибок.
    # Регулировка синаптических весов каждый раз.
    def train(self, inputData, outputData, zeroСonnection, number_of_training_iterations, learningSpeed=0.001):
        for iter in range(number_of_training_iterations):
            # выходы с нейронов послойно
            FeedForwardThroughLayers = []
            FeedForwardThroughLayers.append(inputData)

            arrError = []   # Ошибки синапсов послойно
            arr_l_delta = []   # Матрица коррекции ошибок

            # Получаем выходы с сети
            for i in range(len(self._arraySynapticScales)):
                FeedForwardThroughLayers.append(self._nonlin(np.dot(FeedForwardThroughLayers[-1], self._arraySynapticScales[i])))
                arrError.append([]) #Готовим место для ошибок
                arr_l_delta.append([]) #Готовим место для матрицы коррекции ошибок

            # Идём обратно, и сразу корректируем
            # Последний слой:

            arrError[-1] = outputData - FeedForwardThroughLayers[-1]
            arr_l_delta[-1] = arrError[-1] * self._nonlin(FeedForwardThroughLayers[-1],deriv=True) * learningSpeed

            if (iter% 500) == 0:
                print("Error in " + str(iter) + ' iter :' + str(np.mean(np.abs(arrError[-1]))))
                #learningSpeed = learningSpeed - changeLearningSpeed

            self._arraySynapticScales[-1] += FeedForwardThroughLayers[-2].T.dot(arr_l_delta[-1])

            # Все остальные
            for l in range(len(self._arraySynapticScales) - 1, 0, -1):
                arrError[l-1] = arr_l_delta[l].dot(self._arraySynapticScales[l].T)

                arr_l_delta[l-1] = arrError[l-1] * self._nonlin(FeedForwardThroughLayers[l], deriv=True) * learningSpeed

                self._arraySynapticScales[l - 1] += FeedForwardThroughLayers[l - 1].T.dot(arr_l_delta[l - 1])

            for zeros in zeroСonnection:
                self._arraySynapticScales[zeros[0]][zeros[1]][zeros[2]] = 0

    # Нейронная сеть думает.
    def think(self, inputData):
        # выходы с нейронов послойно
        FeedForwardThroughLayers = []
        FeedForwardThroughLayers.append(inputData)
        # Получаем выходы с сети
        for i in range(len(self._arraySynapticScales)):
            FeedForwardThroughLayers.append(self._nonlin(np.dot(FeedForwardThroughLayers[-1], self._arraySynapticScales[i])))

        return FeedForwardThroughLayers[-1]
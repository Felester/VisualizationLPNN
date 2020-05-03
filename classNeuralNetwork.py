import numpy as np

class NeuralNetwork():
    def __init__(self, seedRandom, NetworkStructure, zeroСonnection):
        # Чтобы контролировать рандом
        np.random.seed(seedRandom)

        #self.arraySynapticScales = np.array([])
        self.arraySynapticScales = []

        # инициализируем веса случайным образом со средним 0
        for i in range(len(NetworkStructure)-1):
            self.arraySynapticScales.append(2*np.random.random((NetworkStructure[i],NetworkStructure[i+1])) - 1)

        #[Слой][нейрон][вес связи к какому нейрону]
        for zeros in zeroСonnection:
            self.arraySynapticScales[zeros[0]][zeros[1]][zeros[2]] = 0

    # Сигмоида
    def nonlin(self, x,deriv=False):
        if(deriv==True):
            return x*(1-x)
        return 1/(1+np.exp(-x))

    # Мы обучаем нейронную сеть в процессе проб и ошибок.
    # Регулировка синаптических весов каждый раз.
    def train(self, inputData, outputData, zeroСonnection, number_of_training_iterations, learningSpeed = 0.001, learningSpeedFinish = 100):

        changeLearningSpeed = 0
        if learningSpeed>learningSpeedFinish:
            changeLearningSpeed = (learningSpeed - learningSpeedFinish)/(number_of_training_iterations/5000)
            #print('Шаг обучение от ', learningSpeed, ' до ', learningSpeedFinish)

        #print('Начали обучение:')

        for iter in range(number_of_training_iterations):

            #выходы с нейронов послойно
            FeedForwardThroughLayers = []
            FeedForwardThroughLayers.append(inputData)

            arrError = []   #Ошибки синапсов послойно
            arr_l_delta = []   #Матрица коррекции ошибок

            # Получаем выходы с сети
            for i in range(len(self.arraySynapticScales)):
                FeedForwardThroughLayers.append(self.nonlin(np.dot(FeedForwardThroughLayers[-1],self.arraySynapticScales[i])))
                arrError.append([]) #Готовим место для ошибок
                arr_l_delta.append([]) #Готовим место для матрицы коррекции ошибок


            # Идём обратно, и сразу корректируем
            # Последний слой:

            arrError[-1] = outputData - FeedForwardThroughLayers[-1]
            arr_l_delta[-1] = arrError[-1] * self.nonlin(FeedForwardThroughLayers[-1],deriv=True) * learningSpeed


            if (iter% 5000) == 0:
                print("Error in " + str(iter) + ' iter :' + str(np.mean(np.abs(arrError[-1]))))
                learningSpeed = learningSpeed - changeLearningSpeed


            self.arraySynapticScales[-1] += FeedForwardThroughLayers[-2].T.dot(arr_l_delta[-1])

            # Все остальные
            for l in range(len(self.arraySynapticScales)-1, 0, -1):
                arrError[l-1] = arr_l_delta[l].dot(self.arraySynapticScales[l].T)

                arr_l_delta[l-1] = arrError[l-1] * self.nonlin(FeedForwardThroughLayers[l], deriv=True) * learningSpeed

                self.arraySynapticScales[l-1] += FeedForwardThroughLayers[l-1].T.dot(arr_l_delta[l-1])

            for zeros in zeroСonnection:
                self.arraySynapticScales[zeros[0]][zeros[1]][zeros[2]] = 0



    # Нейронная сеть думает.
    def think(self, inputData):
    #выходы с нейронов послойно
        FeedForwardThroughLayers = []
        FeedForwardThroughLayers.append(inputData)
        # Получаем выходы с сети
        for i in range(len(self.arraySynapticScales)):
            FeedForwardThroughLayers.append(self.nonlin(np.dot(FeedForwardThroughLayers[-1],self.arraySynapticScales[i])))

        return FeedForwardThroughLayers[-1]

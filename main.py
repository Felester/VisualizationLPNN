import classNeuralNetwork
import MainWindow

layer = 0
NNstruct = [64, 15, 10]
lenKey = NNstruct[layer] * NNstruct[layer+1]


def get_data_sets():
    import pickle
    # Подгружаем данные
    with open('Data\data_1.data', 'rb') as filehandle:
        dataList = pickle.load(filehandle)
    return dataList


def test_nn():
    import numpy as np
    import random
    random.seed(1)
    arrPopulation = [random.randint(0, 1) for i in range(lenKey)]
    dataList = get_data_sets()
    zeroСonnection = []
    for j in range(len(arrPopulation)):
        if arrPopulation[j] == 0:
            zeroСonnection.append([layer, j // NNstruct[layer + 1], j % NNstruct[layer + 1]])

    MyNN = classNeuralNetwork.NeuralNetwork(1, NNstruct, zeroСonnection)
    MyNN.train(dataList[0], dataList[1], zeroСonnection, 25000, 0.1, 0.001)
    prediction = MyNN.think(dataList[2])
    countAnsv = 0;
    for i in range(len(dataList[3])):
        if np.argmax(prediction[i]) == np.argmax(dataList[3][i]):
            countAnsv=countAnsv+1
    print(countAnsv * 100/len(dataList[3]))


if __name__ == "__main__":
    #test_nn()
    mainWin = MainWindow.MainWindow(800, 600, "Визуализатор связей нейронных сетей в процессе обучения")
    mainWin.start_form()

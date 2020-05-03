import numpy as np

def formingKeySet(dataKey):
    result = [[0] * 5 for i in range(len(dataKey))]

    for i in range(len(dataKey)):
        key = int(dataKey[i])
        result[i][key] = 1
    return result


def reading(indexWay):
    f = open("data/dataKey_" + indexWay + ".txt", 'r')
    dataKey = f.read().split("\n")
    del dataKey[-1]

    dataKey = formingKeySet(dataKey)


    f = open("data/dataSet_" + indexWay + ".txt", 'r')
    dataSet = f.read().split("\n")
    del dataSet[-1]

    #каждый кусок выборки переводим из строки в массив чисел, и делим на 255
    for i in range(0, len(dataSet)):
        dataSet[i] = dataSet[i].split(" ")
        del dataSet[i][-1]
        dataSet[i] = [int(item)/255 for item in dataSet[i]]


    dataSet = np.array(dataSet)
    dataKey = np.array(dataKey)
    return dataSet, dataKey

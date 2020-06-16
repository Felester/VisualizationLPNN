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
    MyNN.train(dataList[0], dataList[1], zeroСonnection, 1000, 0.1, 0.001)
    prediction = MyNN.think(dataList[2])
    countAnsv = 0;
    for i in range(len(dataList[3])):
        if np.argmax(prediction[i]) == np.argmax(dataList[3][i]):
            countAnsv=countAnsv+1
    print(countAnsv * 100/len(dataList[3]))


from tkinter import *
def test_canvos_scrol():
    import information_visualizer as iv
    root = Tk()
    frame = LabelFrame(root, text="Конфигурация НС", font=("Comic Sans MS", 10, "bold"))
    frame.place(relwidth=0.98, relheight=0.6, relx=0.01)
    canvas = Canvas(frame, bg='#FFFFFF', width=300, height=300, scrollregion=(0, 0, 1500, 500))
    hbar = Scrollbar(frame, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=canvas.xview)
    canvas.config(width=300, height=300)
    canvas.config(xscrollcommand=hbar.set)
    canvas.pack(side=LEFT, expand=True, fill=BOTH)

    test_iv = iv.InformationAnalyzer()

    image = test_iv.get_rendered_information(400, 800)

    canvas.create_image(25, 25, anchor=NW, image=image)
    canvas.image = image


    root.mainloop()

if __name__ == "__main__":
    #test_nn()
    mainWin = MainWindow.MainWindow(800, 600, "Визуализатор связей нейронных сетей в процессе обучения")
    mainWin.start_form()
    #test_canvos_scrol()






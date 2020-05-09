class DataSetting:
    def __init__(self, data_setting):
        self._NNstruct = data_setting[4]
        self._NNseed = data_setting[0]
        self._zero_connection_seed = data_setting[1]
        self._way_data_set = data_setting[2]
        self._data_set = data_setting[3]
        self._is_run = False


    def get_NNstruct(self):
        return self._NNstruct[1:-1]


    def get_NNseed(self):
        return self._NNseed


    def get_zero_connection_seed(self):
        return self._zero_connection_seed


    def get_way_data_set(self):
        return self._way_data_set



def data_validation(NNstruct, NNseed, zero_connection_seed, way_data_set):
    data_setting = []
    log_validation = ""

    # Проверяем NNseed, чтобы было число
    try:
        data_setting.append(int(NNseed))
        #log_validation += "NNseed в порядке \n"
    except:
        log_validation += "Сид рандома НС не опознан. Необходимо использовать только целые числа \n"

    # Проверяем zero_connection_seed, чтобы было число
    try:
        data_setting.append(int(zero_connection_seed))
        #log_validation += "zero_connection_seed в порядке \n"
    except:
        log_validation += "Сид рандома для обнуления связей не опознан. Необходимо использовать только целые числа \n"

    # Проверяем путь. Есть ли такой файл? Считываем его. Если всё в порядке, сразу проверяем и записываем структуру
    try:
        data_set = _get_data_sets(way_data_set)
        #log_validation += "Путь к данным в порядке, данные выгружены \n"
        data_setting.append(way_data_set)

        if len(data_set) == 4:
            data_setting.append(data_set)
            #print("Структура данных в порядке. Сохранили.")

            NNstruct, log_validation_NNstruct = _NNstruct_validation(NNstruct, data_set)
            if log_validation_NNstruct == "":
                data_setting.append(NNstruct)
            else:
                log_validation += log_validation_NNstruct

        else:
            log_validation += "Структура данных какая то неправильная. Файл повреждён или имеет неверный формат \n"
            log_validation += "Структура не записана, так как файл с данными повреждён"
    except:
        log_validation += "Файл c данными не найден. Проверьте наличие файла по указанному пути \n"



    return data_setting, log_validation

def _NNstruct_validation(NNstruct, data_set):
    log_validation = ""
    try:
        NNstruct = NNstruct.split(" ")
        NNstruct = [int(item) for item in NNstruct]  # Список строк в список чисел

        NNstruct.insert(0, len(data_set[0][0]))
        NNstruct.append(len(data_set[1][0]))
        #log_validation += "Структура записана корректно \n"
    except:
        log_validation += "Структура НС заполнена некорректно \n"
    return NNstruct, log_validation


def _get_data_sets(way):
    import pickle
    # Подгружаем данные
    with open(way, 'rb') as filehandle:
        dataList = pickle.load(filehandle)
    return dataList
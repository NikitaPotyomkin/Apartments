
#функция для парсинга вводных данных, пока абсолютные значения
def inputs():
    inputs_list = []
    max_price = 50000000
    max_square_m2 = ''
    rooms = ''
    time_metro_on_foot = '' #tag: metroTransport = ON_FOOT & timeToMetro = 10
    price_interval = 40000000

    inputs_list.append(max_price) #0
    inputs_list.append(max_square_m2) #1
    inputs_list.append(rooms)  # 2
    inputs_list.append(time_metro_on_foot)  # 3
    inputs_list.append(price_interval)  # 3
    return inputs_list




#sources_used: yandex
#source to be implemented: avito
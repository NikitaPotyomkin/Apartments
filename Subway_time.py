import os
from datetime import date
from selenium import webdriver
import xlsxwriter
import fnmatch
import time
from playsound import playsound
import random
import BS_parser_apartments

try:
    chrome_driver_path = "C:\\Users\Никита\\Dropbox\\BrowserFiles\\chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_path)
except:
    chrome_driver_path = "C:\\Users\Никита\\\Dropbox\\BrowserFiles\\Previous versions\\chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_path)
# create a new Chrome session
driver.implicitly_wait(60)
link = 'https://yandex.ru/maps/213/moscow/?ll=37.530555%2C55.790859&mode=routes'
driver.get(link)

fp = open('Список станций.txt', 'r',encoding='utf-8')
# будем читать строку по 10 байт
line = fp.readline()
lines = []
while line:
    line = fp.readline()
    line = line.rstrip('\n')
    lines.append(line)
times = []
print(lines)
for x in lines:
    try:
        print(x)
        link = 'https://yandex.ru/maps/213/moscow/?ll=37.530555%2C55.790859&mode=routes&rtext='+x+'~Красная площадь'+'&rtt=auto&z=10'
        driver.get(link)
        # print("Нажми enter после подтверждения точки")
        # input()
        route_text = BS_parser_apartments.parse_given_url_bs(driver.current_url)
        # print(route_text)
        for c in route_text:
            if "Без пробок:" in c:
                t1 = c.find('Без пробок:') + len('Без пробок:')
                t2 = c.find('Посмотреть подробнее')
                c = c[t1:t2]
                times.append(x + c)
                break
    except:
        route_time = 'Not found'
        times.append(route_time)
    print(times)




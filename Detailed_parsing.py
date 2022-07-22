from additional_classes import Browser
from additional_classes import Link_to_parse
import pandas as pd
from Functions import score_offers
#для ML модели - нужны колонки метро, площадь, год постройки
#запускаем браузер
pages = 5
offers_driver = Browser().run_browser()
subways_remoteness = pd.read_csv('remoteness.txt', delimiter=",") #получаем файл с удаленностью от центра

#формируем шаблонный линк для парсинга
link = Link_to_parse().create_link() #additional classes.py, вводные параметры в файле Inputs.py
print('Линк с объявлениями:'+link)
#получаем список найденных офферт
offers = []
while len(offers)<1:
    try:
        offers_driver = Browser().run_browser()
        offers = Link_to_parse().browse_links(link,offers_driver,pages)
    except:
        offers_driver.close()
        continue
offers_driver.close()
print(offers)
from selenium import webdriver


chrome_driver_path = "C:\\Users\\Никита\\Dropbox\\BrowserFiles\\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver_path)

driver.implicitly_wait(60)
driver.maximize_window()

# Navigate to the application home page
j = 0
success_offers = []
for offer in offers:
    print(f'----------#{j+1} offer----------')
    # if i>1: break
    link = f"https://realty.yandex.ru/offer/{offer}/"
    try:
        driver.get(link)
    except:
        print(f'error in getting link: {link}')
        continue

    # Click Sing In

    #базовая информация - блок справа, метраж, цена
    print('Базовая информация, блок справа:')
    python_button = driver.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/div[4]/div/div[1]')[0]
    text = python_button.text
    if 'Объявление снято или устарело' in text:
        print('Объявление устарело')
        continue
    j+=1
    square = 0
    total_price = 0
    price_per_meter = 0
    for x in text.split('\n'):
        x = str(x)
        #ищем площадь
        if " м²" in str(x) and square==0:
            square = float(x[:x.find(' м²')].replace(',','.'))
            print('площадь квартиры:' + str(square))
        #ищем цену
        if " ₽" in str(x) and total_price==0:
            total_price = int(x[:x.find(' ₽')].replace(' ',''))
            print('цена квартиры:' + str(total_price))
        #ищем цену за метр
        if " ₽ за м²" in str(x) and price_per_meter==0:
            price_per_meter = int(x[:x.find(' ₽ за м²')].replace(' ',''))
            print('цена за метр:' + str(total_price))

    #catching exceptions
    assert type(square)==float
    assert type(total_price)==int
    assert type(price_per_meter)==int

    #читаем блок базовых параметров (площадь, жилая, кухня, этаж, потолки, год постройки)
    locations_subways = []
    # print('Параметры квартиры:')
    python_button = driver.find_elements_by_xpath('//*[@id="root"]/div[1]/div[2]/div/div[5]/div[2]')[0]
    text = str(python_button.text)
    text = text.replace('\n',',')
    if 'год постройки' in text:
        tag = text.find(' год,год')
        year = text[tag-4:tag]
        assert len(year) == 4
        year = int(year)
    else:
        year = 'undefined'


    #Читаем локацию
    name_subway = 'undefined' #если не найдем
    locations_subways = []
    print('Локация:')
    try:
        python_button = driver.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/div[4]/div/div[1]/div[5]/div[2]')[0]
        text = python_button.text
    except:
        print("location undefined, proceeding")
        continue
    # print(text)
    i = 0
    for x in text.split('\n'):
        # print(x)
        x = str(x)
        if "мин" in x:
            locations_subways.append((text.split('\n')[i-1].strip(),text.split('\n')[i],'пешком'))
            name_subway = locations_subways[0][0]
            assert len(name_subway) >2
        i+=1
    print(locations_subways)
    # получим список станций метро с названием и удаленностью от центра
    if locations_subways !=[]: #если не пусто
        remoteness = subways_remoteness.loc[subways_remoteness['Название станции'] == locations_subways[0][0]]
    else:remoteness = 'undefined'

    try:
        remoteness = round(float(remoteness['Удаленность от центра'].tolist()[0]), 2)
    except:
        remoteness = 100
    success_offers.append([link, total_price, price_per_meter, square, remoteness,year, name_subway])
print(success_offers)
score_offers(success_offers) #в блоке Functions
import Scoring_of_aps
# #нажать Подробнее на описании
# python_button = driver.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/div[5]/div[9]/div/span')[0]
# python_button.click()
# #Читаем описание
# print('Свободное описание:')
# python_button = driver.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/div[5]/div[9]/div/p')[0]
# text = python_button.text
# print(text)
#
#
# #О доме
# print('О доме:')
# python_button = driver.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/div[5]/div[4]')[0]
# text = python_button.text
# print(text)
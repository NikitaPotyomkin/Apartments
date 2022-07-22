#модуль для оценки цен на рынке недвижимости, сорс: Яндекс
from additional_classes import Browser
from additional_classes import Link_to_parse
import Functions
import pandas as pd,time, os, playsound
import datetime
now = datetime.datetime.now()
today_date = str(now)[:10]
#запускаем браузер
test_mode = 'Off' #данные будут читаться из txt, чтобы не открывать браузер
offers = []
pages = 1000
if test_mode !='On':
    open('market_text.txt', 'w').close()
    link = Link_to_parse().create_link() #создаем линк из параметров (Inputs.py)
    print('Линк с объявлениями:'+link)
    driver = Browser().run_browser() #инициализируем браузер
    for page in range(1,pages+1):
        print('page ' +str(page))
        try:
            offers = Link_to_parse().\
            get_prices(link+f'&page{page}',driver) #получаем текст со всеми объявлениями
        except:
            print('page ' +str(page) +' missing')
            continue
        with open("market_text.txt",'a',encoding='utf-8') as f: #записываем полученный текст в файл
            f.write(offers)
        f.close()
        time.sleep(2)

offers = [] #получаем список найденных офферт
with open("market_text.txt",'r',encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        line = line.replace('\n','')
        offers.append(line)
f.close()
squares,prices,subways = [],[],[] #колонки для dataframe
x = 0
for item in offers:
    text = []
    if 'м²,' in item:
        c=x
        while 'Показать телефон' not in offers[c]:
            text.append(offers[c])
            c+=1
        data = Functions.parse_offer_short(text)
        prices.append(data[0]),subways.append(data[1])
    x+=1
assert len(subways) ==len(prices) #убеждаемся, что длины массивов совпадают
# dictionary of lists
price_cn = 'price_'+str(today_date)
dict = {'subway': subways, price_cn: prices}

df = pd.DataFrame(dict)
print(df.shape)
mean_df = df.groupby('subway',as_index=False)[price_cn].mean()

data = {'subway': ['Жоповка'], 'price':[6000]}
test_df = pd.DataFrame(data, index=[0])

base_df = pd.read_csv('real_es_market.csv',encoding='cp1251')
# mean_df = pd.concat([base_df,mean_df],sort=False,axis=1)
mean_df = base_df.merge(mean_df,left_on='subway',right_on='subway',how='outer', suffixes=('', today_date))
# base_df.to_csv('base_df.csv',encoding='cp1251', index=False)
mean_df.to_csv('real_es_market.csv',encoding='cp1251',index=False)

# playsound.playsound('bird.mp3')
import os
os.system("taskkill /im chrome.exe /f")
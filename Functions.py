import pandas as pd

def score_offers(success_offers):
    success_offers.sort(key=lambda x: x[2], reverse=True)
    print('Оцениваем полученные офферы по скоринговой системе')
    #формируем линки
    # for x in success_offers:
    #     x[0] = 'https://realty.yandex.ru/offer/' + x[0]
    #выводим линки на экран
    for x in success_offers:
        print(f'Оффер {x[0]}, по цене за метр {x[2]}, площадью {x[3]}м2')
    #конвертируем массив в датафрейм
    success_offers = pd.DataFrame(success_offers,columns=['Ссылка','Цена','Цена за метр','Площадь',
                                                          'Удаленность_от_метро','Год постройки','Метро'])
    #perform scoring for dataframe

    success_offers.to_excel('Подходящие предложения.xlsx',index = False)
    print(success_offers)


def validate_subway (subway_name,subways_parsed):
    # print(subways_parsed)
    #проверим, что слово двусоставное (ВоронцовскийКалужкская) -и обычно метро идем вторым номером
    #пытаемся понять, есть ли в сплошном слове две заглавные буквы
    i = 0
    count = 0
    an_uppercase_check = False
    for i in range(len(subway_name)-1,0,-1):
        an_uppercase_check = subway_name[i].isupper()
        count+=1
        if subway_name[i] == ' ': break
    if count>1 and an_uppercase_check ==True:
        subway_name = subway_name[len(subway_name)-1-i:]

    #работаем дальше с именем метро
    subway_name = subway_name.replace('»','').replace('«','').replace('.','').replace('"','').replace(',','')
    del subways_parsed[0]
    i = 0
    for x in subways_parsed:
        if subway_name in x:
            subway_name = x
            i +=1
    if i ==0:
        with open('validate_stations.txt','r',encoding='utf-8') as f:
            j = 0
            lines = f.readlines()
            for line in lines:
                if subway_name in line:
                    j+=1
        f.close()
        if j==0:
            with open('validate_stations.txt','a',encoding='utf-8') as file:
                file.write(subway_name+'\n')
            file.close()
    print('валидировать имя:' + subway_name)
    return subway_name


def search_subway_in_text(line):
    numbers = ['123456789']
    new_subway_name = 'Какая то станция'
    i = 0
    for x in line.split():
        if 'мин.ещё' in x:
            subway_name = line.split()[i-2]
            c = 0
            new_subway_name = subway_name[c:]
            for c in range(0,len(subway_name)-1):
                if new_subway_name[0].isupper()==False:
                    new_subway_name = subway_name[c:]
                elif c == len(subway_name)-1:
                    new_subway_name = line.split()[i-2]
                else:
                    break
                c+=1
        i+=1
    new_subway_name = new_subway_name.replace('"','').replace('«','').replace('»','')
    return new_subway_name

def parse_market_text(text):
    print(text)

def parse_offer_short(text):
    # print('parsing')
    c = 0
    info = []
    price,subway = 0,'N'
    for x in text:
        if x [-4:]=='мин.':
            subway = text[c-1].strip()
        if x[-2:] == ' ₽':
            price = int(text[c].replace(' ₽','').replace(' ',''))
        c+=1
    info.append(price), info.append(subway)
    # print(info)
    return info

from Functions import search_subway_in_text
import pandas as pd
f =open("Образец парсинга.txt", "r",encoding='utf-8')
#получим список станций метро с названием и удаленностью от центра
subways_remoteness = pd.read_csv('remoteness.txt', delimiter = ",")
print(subways_remoteness)
def removal_unneeded_words(line):
   line = line.replace('Яндекс.НедвижимостьКабинетДобавить','').replace('объявлениеВойтиКупитьСнятьНовостройкиКоммерческаяИпотекаПрофессионаламПродать квартиру'
                                                                        ,'').replace('ПИКМосква и МОМоскваМосква (без Новой Москвы)','').replace('объявлениеКабинетВойтиКупитьСнятьНовостройкиКоммерческаяИпотекаПрофессионаламЖурналЯ.НедвижимостьМосква','')
   return line

def parse_text(list_parsed, subways_parsed):
   line = "".join(list_parsed)
   line = removal_unneeded_words(line)
   print(line)
   #проверяем если не устарело
   if 'Объявление устарело' in line:
      print('Объявление устарело!')
      return None
   #вычленяем цену
   price1 = line.find("по цене") + len("по цене")
   price2 = line.find("млн")
   price = line[price1:price2]
   print('Цена объекта недвижимости:' + price + 'млн. руб.')

   # вычленяем квадратный метр
   tv = line.find(' ₽ за м²')
   i = 0
   price_per_meter_array = []
   if tv:
      for i in range(tv,0,-1):
         price_per_meter_array.append(line[i])
         if line[i]=='₽' or line[i]=='й':
            break
         i+=1
      # print("символ р за м2:",price_per_meter_array)
   price_per_meter_array.reverse()
   price_per_meter = int(''.join(price_per_meter_array).replace('й','').replace('₽','').replace(' ',''))
   print(f'Цена за квадратный метр: {price_per_meter} м2')

   #вычленяем площадь
   tv = line.find('м²')
   square_numbers =[]
   for s in line:
      square_numbers.append(line[tv-2:tv-1])
      tv = tv - 1
      if line[tv-2:tv-1] ==' ':
         break
   square_numbers.reverse()
   square = float(''.join(square_numbers).replace(',','.'))
   print(f'Площадь объекта: {square} м2')

   #вычленяем метро
   i = 0
   for m in line.split():
      metro = ''
      if 'метро' in m:
         # print(line.split())
         metro = line.split()[i+1].replace('Купить','')
         #проверяем, зацепили ли мы двухсоставное название метро
         if "«" in metro and '»' not in metro:
            metro = line.split()[i + 1].replace('Купить', '') + ' '+ line.split()[i + 2]
         if '"' in metro and '"' not in metro:
            metro = line.split()[i + 1].replace('Купить', '') + ' '+ line.split()[i + 2]
         if '«' not in metro:
            if '"' not in metro:
               metro = 'Не определено'
         break
      i+=1
   if metro == '' or metro =='Не определено':
      metro = search_subway_in_text(line)
   from Functions import validate_subway
   metro = validate_subway(metro,subways_parsed)
   remoteness =subways_remoteness.loc[subways_remoteness['Название станции'] == metro]
   try:
      remoteness = round(float(remoteness['Удаленность от центра'].tolist()[0]),2)
   except IndexError:
      remoteness = 0
   print('Удаленность от метро:' + str(remoteness))
   print(f'Метро объекта:{metro}')

   #расстояние до метро - предлагаю руками создать базу
   print('Расстояние до метро:')
   return price,square,price_per_meter,remoteness

# f = parse_text(f)

# def parse_text(list_parsed):
#    square = 0
#    line = "".join(list_parsed)
#    print(line)
#    #вычленяем цену
#    price1 = line.find("по цене") + len("по цене")
#    price2 = line.find("млн")
#    price = line[price1:price2]
#    print('Цена объекта недвижимости:' + price + 'млн. руб.')
#    print('Площадь объекта:' + 'м2')
#    print('Метро объекта:')
#    print('Расстояние до метро:')
#    return price,square
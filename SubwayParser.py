# source https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%81%D1%82%D0%B0%D0%BD%D1%86%D0%B8%D0%B9_%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BC%D0%B5%D1%82%D1%80%D0%BE%D0%BF%D0%BE%D0%BB%D0%B8%D1%82%D0%B5%D0%BD%D0%B0
#http://www.lovrikinfo.ru/metrogps.php

import pandas as pd
pd.set_option('display.max_rows', 500)
#center point
Red_Square_шир = 55.7538
Red_Square_дол = 37.6211812

subways_table = pd.read_excel(r'C:\Users\Никита\Dropbox\PycharmProjects\Apartments\Subways\Subways.xlsx',engine='openpyxl')


subways_table["Широта"] = subways_table["Широта"].astype(float)

subways_table["Долгота"] = subways_table["Долгота"].astype(float)

subways_table['Удаленность от центра'] = 100*round(abs(subways_table['Широта']-Red_Square_шир)\
                                         +abs(subways_table['Долгота']-Red_Square_дол),4)

remoteness = subways_table[['Ветка', 'Название станции', 'Удаленность от центра']].copy()
remoteness.to_csv(r'remoteness.txt', header=True, index=None, sep=',', mode='a')
print(subways_table)

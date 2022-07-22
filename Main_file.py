import os
from datetime import date
from selenium import webdriver
import xlsxwriter
import fnmatch
from Functions import score_offers

from additional_classes import Browser
from additional_classes import Link_to_parse

#запускаем браузер
pages = 1
driver = Browser().run_browser()

#формируем шаблонный линк для парсинга
link = Link_to_parse().create_link() #additoinal classes.py

#получаем список найденных офферт
offers = Link_to_parse().browse_links(link,driver,pages)

print('Подобранные для вас объявления:')
#сортируем массив по цене

#оцениваем полученный массив квартир по рейтинговой системе
score_offers(offers)    #Functions.py
import Scoring_of_aps
from selenium import webdriver
import Inputs
import time

class Browser:
    def __init__(self):
        self.chrome_driver_path = "C:\\Users\\Никита\\Dropbox\\BrowserFiles\\chromedriver.exe"

    def run_browser(self):
        try:
            driver = webdriver.Chrome(self.chrome_driver_path)
        except:
            driver = webdriver.Chrome(self.chrome_driver_path)
        # create a new Chrome session
        driver.implicitly_wait(60)
        return driver

class Link_to_parse():
    def __init__(self):
        self.inputs = Inputs.inputs()
        self.input_max_price = self.inputs[0]

    def create_link(self):
        '''create link out of inputs'''
        #creating price_tag
        if self.input_max_price!=0:
            price_tag = f"&priceMin={self.input_max_price-self.inputs[4]}&priceMax={self.input_max_price}"
        else:
            price_tag = ''
        #creating square_tag
        input_max_square = self.inputs[1]
        if input_max_square!=0:
            square_tag = f"&areaMax={input_max_square}"
        else:
            square_tag = ''

        #требование до метро?
        input_metro_by_foot = self.inputs[3]
        if input_metro_by_foot!=0:
            foot_metro_tag = f"&metroTransport=ON_FOOT&timeToMetro={input_metro_by_foot}"
        else:
            foot_metro_tag = ''


        self.link = f"https://realty.yandex.ru/moskva_i_moskovskaya_oblast/kupit/kvartira/?utm_campaign=brand.prod_realty&" \
               f"utm_medium=brand&utm_source=wizard{price_tag}{square_tag}{foot_metro_tag}"
        return self.link

    def browse_links(self,link,driver,last_page):
        # initializing variables
        #страницы с объявлениями, старт
        i = 0
        #инициализируем списки
        subways = []
        minutes = []
        ad_slots = [4, 8, 13, 18, 23]
        success_offers = []
        import pandas as pd

        # итерируемся постранично
        offers = []
        for i in range(0,last_page):
            print('-----Открываем страницу ' + str(i + 1) + '-----')
            driver.get(link + f"&page={str(i)}")
            print('Сохраняем ' + str(i + 1) + ' страницу в txt файл')
            with open('page' + str(i) + '.txt', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            with open('page' + str(i) + '.txt', 'r', encoding='utf-8') as f:
                text = f.readlines()
                for x in text:
                    if '/offer.' in x:
                        x = x.split()
                        for c in x:
                            if 'href="/offer/' in c:
                                c = c.replace('/?isExact=YES"', '').replace('href="/offer/', '').replace('/"', '')
                                c = c.replace('/?isExact=NO"', '').replace('href="/offer/', '').replace('/"', '')
                                offers.append(c)
                        break
            # убираем новые всплывшие символы
            i = 0
            for i in range(0, len(offers)):
                offers[i] = offers[i].replace('/?isExact=NO&amp;source=serp_offers_item"', '')
                offers[i] = offers[i].replace('/?isExact=YES&amp;source=serp_offers_item"', '')
                i += 1
            offers = list(set(offers))
        return offers

    def get_prices(self,link,driver):
        driver.get(link)
        field = driver.find_elements_by_xpath('//*[@id="root"]/div[2]/div[2]/div[2]/div[2]/div')[0]
        return(field.text)



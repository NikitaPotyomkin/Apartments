import urllib
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import date
from collections import Counter
import unicodedata

def parse_given_url_bs(url):
    with open(url, 'rb') as html:
        soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk).replace('\xa0', ' ')
    text = text.splitlines()
    return text
# a =parse_given_url_bs('https://yandex.ru/maps/213/moscow/?ll=37.530555%2C55.790859&mode=routes&rtext=55.601177%2C37.407995~55.753600%2C37.621094&rtt=auto&ruri=ymapsbm1%3A%2F%2Fgeo%3Fll%3D37.408%252C55.601%26spn%3D0.001%252C0.001%26text%3D%25D0%25A0%25D0%25BE%25D1%2581%25D1%2581%25D0%25B8%25D1%258F%252C%2520%25D0%259C%25D0%25BE%25D1%2581%25D0%25BA%25D0%25B2%25D0%25B0%252C%2520%25D0%25A1%25D0%25BE%25D0%25BA%25D0%25BE%25D0%25BB%25D1%258C%25D0%25BD%25D0%25B8%25D1%2587%25D0%25B5%25D1%2581%25D0%25BA%25D0%25B0%25D1%258F%2520%25D0%25BB%25D0%25B8%25D0%25BD%25D0%25B8%25D1%258F%252C%2520%25D0%25BC%25D0%25B5%25D1%2582%25D1%2580%25D0%25BE%2520%25D0%25A4%25D0%25B8%25D0%25BB%25D0%25B0%25D1%2582%25D0%25BE%25D0%25B2%2520%25D0%259B%25D1%2583%25D0%25B3~ymapsbm1%3A%2F%2Fgeo%3Fll%3D37.621%252C55.754%26spn%3D0.006%252C0.003%26text%3D%25D0%25A0%25D0%25BE%25D1%2581%25D1%2581%25D0%25B8%25D1%258F%252C%2520%25D0%259C%25D0%25BE%25D1%2581%25D0%25BA%25D0%25B2%25D0%25B0%252C%2520%25D0%259A%25D1%2580%25D0%25B0%25D1%2581%25D0%25BD%25D0%25B0%25D1%258F%2520%25D0%25BF%25D0%25BB%25D0%25BE%25D1%2589%25D0%25B0%25D0%25B4%25D1%258C&z=10')
# print(a)
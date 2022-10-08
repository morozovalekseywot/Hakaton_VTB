import json
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait


def is_news(x):
    x = str(x)
    if x is None:
        return False
    else:
        if x.startswith("/business"):
            return True
        return False


url = r"https://www.interfax.ru/business/"
resp = requests.get(url)

# profile_path = r'C:\Users\ujifv\AppData\Roaming\Mozilla\Firefox\Profiles\ojy7pkea.default'
profile_path = r'C:\Users\Diablo\AppData\Roaming\Mozilla\Firefox\Profiles\x0prq2bw.default'
options = Options()
options.set_preference('profile', profile_path)
driver = Firefox(options=options)
driver.get(url)
driver.implicitly_wait(20)
cookies = driver.find_element("xpath", "/html/body/div[8]/span")
cookies.click()

for i in range(10):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "timeline__more"))
        )
        driver.implicitly_wait(2)
        button = driver.find_element(By.CSS_SELECTOR, ".timeline__more")
        # html body.landscape.scrolled main div.mainblock div.leftside div.timeline__btnsgroup div.timeline__more
        button.click()
        driver.implicitly_wait(10)  # in seconds
    except:
        break

driver.implicitly_wait(10)
resp = driver.page_source
driver.close()

soup = BeautifulSoup(resp, 'lxml')
links = [link.get('href') for link in soup.find_all('a')]
news_link = list(filter(is_news, list(set(links))))
news_link = list(map(str, news_link))
clear_news = []
data = []
headers = []
urls = []

print(len(news_link))

for link in news_link:
    req = requests.get(url[:-9] + link)
    urls.append(url[:-9] + link)
    # print(url[:-9] + link)
    if req.status_code == 200:
        try:
            soup = BeautifulSoup(req.text, "lxml")
            ans = soup.find("article", {"itemprop": "articleBody"})
            headers.append(soup.find("h1", {"itemprop": "headline"}).text)
            clear_news.append(ans.text.strip())
            date = soup.find("a", {"class": "time"}).text.strip()
            data.append(date[date.find("news"):].replace("/", "."))
        except:
            continue

news = {i: {"url": urls[i], "header": headers[i].replace("\u2192", "-").replace("\u22c5", ' '),
            "date": data[i].replace("\u2192", "-").replace("\u22c5", ' '), "news": clear_news[i].replace("\u2192", "-").replace("\u22c5", ' ')} for i in range(len(data))}

with open("interfax_news.json", "w", encoding='ISO-8859-1') as out:
    out.write(json.dumps(news, ensure_ascii=False))
#
# print(len(news))

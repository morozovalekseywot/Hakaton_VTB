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

profile_path = r'C:\Users\Diablo\AppData\Roaming\Mozilla\Firefox\Profiles\x0prq2bw.default'
options = Options()
options.set_preference('profile', profile_path)
# service = Service(r'D:\python\VTB_tricks\geckodriver.exe')
driver = Firefox(options=options)
driver.get(url)
# button = driver.find_element_by_xpath("button__item button__item_listing")
cookies = driver.find_element_by_xpath("/html/body/div[8]/span")

cookies.click()
# button = driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/a")
for i in range(4):
    element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "arrow__down"))
    )
    driver.implicitly_wait(2)
    button = driver.find_element_by_class_name("arrow__down")
    button.click()
    # driver.implicitly_wait(10)  # in seconds

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

    if url.endswith(r"\world"):
        req = requests.get(url[:-6] + link)
        urls.append(url[:-6] + link)
    else:
        req = requests.get(url[:-9] + link)
        urls.append(url[:-9] + link)
    # print(url[:-9] + link)
    if req.status_code == 200:
        try:
            soup = BeautifulSoup(req.text, "lxml")
            ans = soup.find("article", {"itemprop": "articleBody"})
            headers.append(soup.find("h1", {"itemprop": "headline"}).text)
            # print(ans.text)
            clear_news.append(ans.text.strip())
            date = soup.find("a", {"class": "time"}).text.strip()
            data.append(date[date.find("news"):].replace("/", "."))
        except:
            continue

news = {i: {"url": urls[i], "header": headers[i], "date": data[i], "news": clear_news[i]} for i in range(len(data))}

with open("interfax_news.json", "w", encoding='utf-8') as out:
    out.write(json.dumps(news, ensure_ascii=False))

print(len(news))

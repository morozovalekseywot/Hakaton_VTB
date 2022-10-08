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
        if x.count("ria.ru/20") != 0:
            return True
        return False


url = r"https://ria.ru/economy/"
resp = requests.get(url)

profile_path = r'C:\Users\ujifv\AppData\Roaming\Mozilla\Firefox\Profiles\ojy7pkea.default'
options = Options()
options.set_preference('profile', profile_path)
driver = Firefox(options=options)
driver.get(url)
driver.implicitly_wait(1000)

try:
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[11]/div/div/div[4]/div/div[1]/div[4]"))
    )
    cookies = driver.find_element(By.XPATH, "/html/body/div[11]/div/div/div[4]/div/div[1]/div[4]")
    cookies.click()
except:
    driver.implicitly_wait(2)

for i in range(100):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[10]/div[2]/div/div[4]/div/div[1]/div/div[3]"))
    )
    # driver.implicitly_wait(5)
    count = 0
    while count < 15:
        try:
            button = driver.find_element(By.XPATH, "/html/body/div[10]/div[2]/div/div[4]/div/div[1]/div/div[3]")
            button.click()
            break
        except:
            count += 1
            driver.implicitly_wait(30)

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

    req = requests.get(link)
    if len(data) % 100 == 0:
        print(len(data))
    if req.status_code == 200:
        try:
            soup = BeautifulSoup(req.text, "lxml")
            ans = soup.findAll("div", {"class": "article__text"})
            headers.append(soup.find("div", {"class", "article__title"}).text)
            # print(ans.text)
            str_news = ""
            for n in ans:
                str_news += n.text

            clear_news.append(str_news)
            date = soup.find("div", {"class": "article__info-date"}).text.strip()
            data.append(date.split(" ")[1])
            urls.append(link)
        except:
            continue

news = {i: {"url": urls[i], "header": headers[i], "date": data[i], "news": clear_news[i]} for i in range(len(data))}
#
with open("ria.json", "w", encoding='utf-8') as out:
    out.write(json.dumps(news, ensure_ascii=False))

print(len(news))

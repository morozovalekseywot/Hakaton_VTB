import json

import requests
from bs4 import BeautifulSoup


def is_news(x):
    x = str(x)
    if x is None or (not x.endswith(".html") or x.find("ria") == -1):
        return False
    else:
        if x[x.index("ria.ru/") + 8].isdigit():
            return True
        return False


url = r"https://ria.ru/economy/"
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'lxml')
links = [link.get('href') for link in soup.find_all('a')]

news_link = filter(is_news, list(set(links)))
d = {'news': []}
for link in list(news_link):
    # print(link)
    req = requests.get(link)
    if req.status_code == 200:
        soup = BeautifulSoup(req.text, "lxml")
        ans = soup.findAll("div", {"class": "article__text"})
        data = soup.find("div", {"class": "article__info-date"})
        mini = {}
        str_news = ""
        for n in ans:
            str_news += n.text
        # print(data.text.split()[1])
        mini['text'] = str_news
        mini['date'] = data.text.split()[1]
        mini['url'] = link
        d['news'].append(mini)

with open("data.txt", "w", encoding="cp437") as out:
    for item in d['news']:
        for k, v in item.items():
            print(v)
        print(20 * '-')

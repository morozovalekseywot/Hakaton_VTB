import json

import requests
from bs4 import BeautifulSoup

# url = "https://newsapi.org/v2/top-headlines?country=ru&from=2022-09-07&apiKey=435dbcbf941941189bb7556341b1075d"
# url = "https://ria.ru/organization_API/"

with open('ria.html', "r", encoding="cp437") as file:
    src = file.read()
soup = BeautifulSoup(src, "lxml")
ans = soup.findAll("div", {"class": "article__text"})
with open("data.txt", "w", encoding="cp437") as out:
    for a in ans:
        out.write(a.text)
# resp = requests.get(url).json()
# print(resp)
# if resp['status'] != "ok":
#     print(resp)
# # print(resp)
#
# data = {'news': []}
#
# names = set()
# for res in resp['articles']:
#     if res['source']['name'] in ["Kommersant.ru"]:
#         d = {'title': res['title'], 'url': res['url'], 'data': res['publishedAt']}
#         # data['news'].append(d)
#     names.add(res['source']['name'])
#
# print(names)

# with open('data.json', 'w') as outfile:
#     json.dump(data, outfile)

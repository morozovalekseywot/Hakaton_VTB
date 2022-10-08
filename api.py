#!flask/bin/python
import json
import datetime

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'pigs'
    if username == "user":
        return "pass"
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


class News:
    # def __init__(self, id_, topic, title, url, to, date):
    #     self.id = id_
    #     self.topic = topic
    #     self.title = title
    #     self.url = url
    #     self.to = to
    #     self.date = date

    def __init__(self, json_data):
        self.id = json_data["id"]
        self.topic = json_data["Topic"]
        self.title = json_data["Title"]
        self.url = json_data["URL"]
        self.to = json_data["To"]
        self.date = json_data["Date"]
        self.rating = json_data["Rating"]

    def __str__(self):
        return "id: " + self.id + "\nTitle: " + self.title + "\nURL: " + self.url


def get_all_news(who, date, is_politics, count):
    with open('news.json') as json_file:
        data = json.load(json_file)
        filtered_news = []
        if is_politics:
            for news in data['News']:
                print(news)
                if int(news['Date']) >= date and (int(news['To']) == who or int(news['To']) == 3):
                    filtered_news.append(news)
        else:
            for news in data['News']:
                if news['Topic'] != "Политика" and int(news['Date']) >= date and (
                        int(news['To']) == who or int(news['To']) == 3):
                    filtered_news.append(news)

        if len(filtered_news) > count:
            sorted(filtered_news, key=lambda news_: news_['Rating'])
            return filtered_news[-count:]
        else:
            return filtered_news


def make_public_news(news):
    new_news = []
    for n in news:
        d = {'URL': n['URL'], 'Topic': n['Topic'], "Title": str(n["Title"]).strip(),
             "Date": str(datetime.date.fromtimestamp(n['Date']))}
        new_news.append(d)
    return new_news


# <string:date>&<int:is_politics>&<int:who>
@app.route('/vtb/api/v1.0/news', methods=['GET'])
@auth.login_required
def get_news():
    req = request.args
    # print(req)
    date = req['date']
    is_politics = int(req['is_politics'])
    who = int(req['who'])
    count = int(req.get("count", 3))
    # date = 07.10.2022
    if is_politics == 1:
        is_politics = True
    else:
        is_politics = False
    dates = list(map(int, date.split(".")))
    date = datetime.date(dates[2], dates[1], dates[0])
    date = datetime.datetime.fromisoformat(date.isoformat())

    return json.dumps({'news': make_public_news(get_all_news(who, date.timestamp(), is_politics, count))},
                      ensure_ascii=False, separators=(',\n', ': '))


# curl -u admin:pigs -i "http://127.0.0.1:5000/vtb/api/v1.0/news?date=05.10.2022&is_politics=1&who=1"
if __name__ == '__main__':
    app.run(debug=True)

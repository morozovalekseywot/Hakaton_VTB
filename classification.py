import json
import matplotlib.pyplot as plt
import pymorphy2

morph = pymorphy2.MorphAnalyzer(lang='ru')

with open('razmet.json', encoding='utf-8') as f:
    data = json.load(f)

# n = 4
# count = [0] * n
# for i, d in data.items():
#     count[d['to']] += 1
#
# names = ['никто', 'директор', 'бухгалтер', 'оба']
# for i in range(n):
#     names[i] = names[i] + " (" + str(count[i]) + ")"
#
# plt.rcParams['figure.figsize'] = (10, 8)
# plt.rcParams['font.size'] = '14'
#
# plt.bar(range(4), count)
# plt.xticks(range(4), names)
# plt.ylabel('Number of class elements')
# plt.xlabel('Classes')
# plt.title("Distribution histogram")
# plt.show()

print(len(data))

# https://pymorphy2.readthedocs.io/en/stable/user/grammemes.html
stopwords = ['NPRO', 'PREP', 'CONJ', 'PRCL', 'INTJ']


def make_bag(text):
    text = text.lower()
    new_text = ""
    for s in text:
        if s.isalpha() or s.isnumeric() or s in " -$₽₿£¥€#@()%+":
            new_text += s
    words = new_text.split()
    total_words = set()
    for word in words:
        parsed_word = morph.parse(word)[0]
        if parsed_word.tag.POS in stopwords:
            continue
        total_words.add(parsed_word.normal_form)
    return total_words


# Среднее соответствие внутри классов
sum_to1 = 0
count_to1 = 0

sum_to2 = 0
count_to2 = 0

for i1, d1 in data.items():
    print(int(i1), "/", len(data))
    d1_bag = make_bag(d1['news'])
    for i2, d2 in data.items():
        if int(i1) >= int(i2):
            continue
        d2_bag = make_bag(d2['news'])
        score = len(d1_bag.intersection(d2_bag)) / len(d1_bag.union(d2_bag))
        if d1['to'] == d2['to'] == 1:
            sum_to1 += score
            count_to1 += 1
        elif d1['to'] == d2['to'] == 2:
            sum_to2 += score
            count_to2 += 1

print(sum_to1)  #
print(count_to1)  #
print(sum_to2)  #
print(count_to2)  #

# Разбиваем на тест и трейн
#
# test = dict()
# train = dict()
#
# count = 0
# for i, d in data.items():
#     if int(i) >= len(data) * 0.2:
#         train[i] = d
#     else:
#         test[i] = d
#
# print(len(test))
# print(len(train))


# Предсказываем для теста
#
# entry_to1 = 0.5
# entry_to2 = 0.5
#
# true = list()
# predicted = list()
#
# for i1, d1 in test.items():
#     print(int(i1), "/", len(test))
#     true.append(d1['to'])
#     d1_bag = make_bag(d1['news'])
#     sum_pred1 = 0
#     sum_pred2 = 0
#     count_scores = 0
#     for i2, d2 in train.items():
#         d2_bag = make_bag(d2['news'])
#         score = len(d1_bag.intersection(d2_bag)) / len(d1_bag.union(d2_bag))
#         count_scores += 1
#         if d2['to'] == 1:
#             sum_pred1 += score
#         elif d2['to'] == 2:
#             sum_pred2 += score
#         elif d2['to'] == 3:
#             sum_pred1 += score
#             sum_pred2 += score
#     p_to1 = sum_pred1 / count_scores
#     p_to2 = sum_pred2 / count_scores
#
#     if p_to1 >= entry_to1 and p_to2 >= entry_to2:
#         predicted.append(3)
#     elif p_to1 >= entry_to1:
#         predicted.append(1)
#     elif p_to2 >= entry_to2:
#         predicted.append(2)
#     else:
#         predicted.append(0)
#
# print(true)
# print(predicted)

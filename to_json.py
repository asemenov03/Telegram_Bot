import json


with open('stopwords.txt', encoding='utf-8') as r:
    ar = r.read()
    ar = ar.split(' ')
print(len(ar))
with open('stopwords.json', 'w', encoding='utf-8') as e:
    json.dump(ar, e)

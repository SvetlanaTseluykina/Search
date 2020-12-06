from datetime import datetime
from elasticsearch import Elasticsearch
import json

months = ['\\u044f\\u043d\\u0432\\u0430\\u0440\\u044f', '\\u0444\\u0435\\u0432\\u0440\\u0430\\u043b\\u044f', '\\u043c\\u0430\\u0440\\u0442\\u0430', '\\u0430\\u043f\\u044\\u0435\\u043b\\u044f', '\\u043c\\u0430\\u044f', '\\u0438\\u044e\\u043d\\u044f', '\\u0438\\u044e\\u043b\\u044f', '\\u0430\\u0432\\u0433\\u0443\\u0441\\u0442\\u0430', '\\u0441\\u0435\\u043d\\u0442\\u044f\\u0431\\u0440\\u044f', '\\u043e\\u043a\\u0442\\u044f\\u0431\\u0440\\u044f', '\\u043d\\u043e\\u044f\\u0431\\u0440\\u044f', '\\u0434\\u0435\\u043a\\u0430\\u0431\\u0440\\u044f']

es = Elasticsearch()

doc = {
    'url': 'url',
    'title': 'title',
    'story': 'story',
    'timestamp': datetime(2020, 11, 10, 10, 10, 0)
}


res = es.index(index="newsvl", id=1, body=doc)

arr = []
file = open('newsvl.json', 'r')
while True:
    line = file.readline()
    if len(line) == 0:
        break
    if not line == "[\n" and not line == "][\n" and not line == "]":
        if line[len(line)-2] == ",":
            line = line[:len(line)-2]
        ind = line.find("datetime") + 11
        dtm = line[ind:].split("\"")
        hh = 0
        mm = 0
        dd = 0
        mo = 0
        yy = 0
        ss = dtm[1].split(' ')
        if len(ss) >= 4:
             time = ss[0].split(':')
             hh = int(time[0])
             mm = int(time[1][0:len(time[1])-1])
             dd = int(ss[1])
             mo = int(months.index(ss[2].encode('utf-8').decode('utf-8')) + 1)
             yy = int(ss[3])
        else:
            print(ss)
        line = line[:line.find("datetime") - 1] + "\"timestamp\": \"" + str(datetime(yy, mo, dd, hh, mm)).replace(" ", "T") + "\"" + dtm[2]
        decoded = json.loads(line)
        arr.append(decoded)
file.close()

i = 2
for item in arr:
    es.index(index="newsvl", id=i, body=arr[i-2])
    i += 1

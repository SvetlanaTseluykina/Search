from elasticsearch import Elasticsearch


print("Введите строку, которую надо найти:")
srch = input()
while not srch or srch.isspace():
    print("Введите строку, которую надо найти:")
    srch = input()

print("Введите дату и время начала для фильтрации в формате yyyy-mm-dd-Thh:mm:ss (можно оставить пустым):")
dtm1 = input()

dtm2 = ""
if dtm1:
    print("Введите дату и время конца для фильтрации в формате yyyy-mm-dd-Thh:mm:ss")
    dtm2 = input()
    while not dtm2 or dtm2.isspace():
        print("Введите дату и время конца для фильтрации в формате yyyy-mm-dd-Thh:mm:ss")
        dtm2 = input()

es = Elasticsearch()

es.indices.refresh(index="test")

size = 10000

if not dtm1:

    query_body = {
        "query": {
                "match": {
                    "title": srch
            }
        }
    }
else:
    query_body = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                    "title": srch
                    }
                },
       "filter":{
            "range": {
            "timestamp": {
                 "gte": dtm1,
                 "lte": dtm2
                         }
                }
            }
        }
    }
}


res = es.search(index="newsvl", body=query_body, size=size)
print("All these links were found:")
for hit in res['hits']['hits']:
    print("%(url)s" % hit["_source"], "score: ", hit["_score"])
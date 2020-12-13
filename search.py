from elasticsearch import Elasticsearch
import requests
import re


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

token = 'dict.1.1.20201208T073341Z.f546b7f91275394c.c8e2d40ca91ea58d6b2bf00fde795397294c9215'
url = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'
out = ''

all_words = srch.split(' ')
for every_word in all_words:
    synonyms_option = {'key': token, 'lang': 'ru-ru', 'text': every_word}
    webRequest = requests.get(url, params=synonyms_option)
    regex_num = re.compile('(?<={"text"):"(.+?)"(?=,)')
    matcher = regex_num.findall(webRequest.text)
    out += every_word
    if len(matcher) == 0:
        out += '\r'
    else:
        out += ', '
        for i in range(1, len(matcher) - 1):
            out += matcher[i] + ', '
        out += matcher[len(matcher) - 1] + '\r'

file = open('/etc/elasticsearch/synonyms.txt', 'w')
file.write(out)
file.close()

# #print(matcher)
#
es = Elasticsearch()

es.indices.refresh(index="newsvl")

my_settings = {
   "settings": {
     "analysis": {
       "filter": {
        "synonym_filter": {
              "type": "synonym",
              "synonyms_path": "synonyms.txt",
        },
         "ru_stop": {
          "type": "stop",
           "stopwords": "_russian_"
        },
         "ru_stemmer": {
           "type": "snowball",
           "language": "Russian"
         }
       },
       "analyzer": {
         "default": {
           "char_filter": [
             "html_strip"
           ],
          "tokenizer": "standard",
           "filter": [
               "synonym_filter",
               "lowercase",
               "ru_stop",
               "stemmer"
           ]
         }
       }
     }
   },
   "mappings": {
     "post": {
       "properties": {
        "url": {
             "type": "string",
         },
         "story": {
            "type": "string"
        },
        "timestamp": {
            "type": "date"
        },
        "title": {
           "type": "string",
           "analyzer": "default"
         }
       }
     }
   }
 }

es.indices.close(index="newsvl")
es.indices.put_settings(my_settings, index="newsvl")
es.indices.open(index="newsvl")

es.indices.refresh(index="newsvl")

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
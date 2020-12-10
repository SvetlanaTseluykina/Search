from datetime import datetime

from elasticsearch import Elasticsearch

es = Elasticsearch()

my_settings = {
   "settings": {
     "analysis": {
       "filter": {
         "ru_stop": {
          "type": "stop",
           "stopwords": "_russian_"
        },
         "ru_stemmer": {
           "type": "snowball",
           "language": "Russian"
         },
         "synonym_filter": {
             "type": "synonym_graph",
             "synonyms": ["приморье, владивосток",
                         "мост, строение, сооружение",
                         "дом, здание, постройка",
                         "снег, мороз, лёд, дождь, погода",
                         "житель, жительница, горожанин, человек",
                         "администрация, управление, власть",
                         "трасса, дорога, шоссе",
                         "автомобиль, машина",
                          "новый год, праздник, рождество, каникулы, отдых",
                          "пожар, огонь, дым"]

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


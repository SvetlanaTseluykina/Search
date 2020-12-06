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
           "type": "stemmer",
           "language": "russian"
         }
       },
       "analyzer": {
         "default": {
           "char_filter": [
             "html_strip"
           ],
          "tokenizer": "standard",
           "filter": [
             "lowercase",
             "ru_stop",
             "ru_stemmer"
           ]
         }
       }
     }
   },
   "mappings": {
     "post": {
       "properties": {
         "parent_url": {
             "type": "string",
         },
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
           "index": "not_analyzed"
         }
       }
     }
   }
 }

es.indices.close(index="newsvl")
es.indices.put_settings(my_settings, index="newsvl")
es.indices.open(index="newsvl")


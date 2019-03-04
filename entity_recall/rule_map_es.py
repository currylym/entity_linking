
import json
from collections import Counter

from elasticsearch import Elasticsearch
es = Elasticsearch()
'''
mapping = {
           "mappings":{
             "abbreviation_map":{
               "properties":{
                 "abbreviation_key":{ "type": "text" },
                 "related_full_name_with_frequency":{ "type": "text" }
                }
              }
            }
          }
'''
def write_json_to_es(json_path):

    def _json_transform(json_data):
        for key,value in json_data.items():
            value_frequency = dict(Counter(value))
            value_frequency = {k:v/len(value) for k,v in value_frequency.items()}
            if len(value) <= 20:
                yield {'abbreviation_key':key,'related_full_name_with_frequency':json.dumps(value_frequency,ensure_ascii=False)}

    json_data = json.loads(open(json_path).read())
    for index,doc in enumerate(_json_transform(json_data)):
        es.index(index="rule", doc_type='abbreviation_map', id=index, body=doc)
    
    es.indices.refresh(index="rule")
    print('write local json to es!')

def es_search_rulemap(query,size=5):
    res = es.search(index="rule", doc_type='abbreviation_map', body={"query": {"match": {"abbreviation_key":query}}},size=size)
    hits = []
    for hit in res['hits']['hits']:
        source = json.loads(hit["_source"]["related_full_name_with_frequency"])
        for key,value in source.items():
            hits.append({'name':key,'score':value*hit['_score']})
    hits = sorted(hits,key=lambda x:-x['score']) 
    return hits

if __name__ == '__main__':
    #write_json_to_es('abbreviation_alignment.json')
    hits = es_search_rulemap('北京汽车')
    print(hits)


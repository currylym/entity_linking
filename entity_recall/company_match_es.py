
from elasticsearch import Elasticsearch
es = Elasticsearch()

def es_search(query,size=5):
    res = es.search(index="company_names", doc_type='company_to_es', body={"query": {"match": {"name":query}}}, size=size)
    hits = []

    for hit in res['hits']['hits']:
        source = hit["_source"]
        source['es_score'] = hit["_score"]
        hits.append(source)

    #print(hits)
    return hits

if __name__ == '__main__':
    print(es_search(query='上汽'))

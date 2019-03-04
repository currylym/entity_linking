
import json
import sys
sys.path.append('..')

from entity_recall.rule_map_es import es_search_rulemap
from entity_recall.company_match_es import es_search
from entity_recall.baike_recall import BaiduBaike
from config import config

#
myconfig = config()
baidu = BaiduBaike(check_url="http://baike.baidu.com/item/李白")

def entity_recall(query,sizes=[5,20],mode='baike'):
    '''
    params:
    -------
    query:
    sizes:
    mode:
    '''
    res = {}
    if mode == 'map' or mode == 'all':
        res['rule_map'] = es_search_rulemap(query,sizes[0])
    if mode == 'match' or mode == 'all':
        res['str_match'] = es_search(query,sizes[1])
    if mode == 'baike' or mode == 'all':
        res['baike_entry'] = baidu.info_extract_baidu(query)

    #print(json.dumps(res,indent=1,ensure_ascii=False))
    return res

#对部分测试数据先进行entity recall
def main(num=10):
    test_data = json.loads(open(myconfig.test_data_path).read())
    res = []
    for i in range(num):
        data = test_data[i]
        text = data['text']
        annotations = data['annotation']
        for annotation in annotations:
            annotation['text'] = text    
            annotation['my_entity_recall'] = entity_recall(annotation['mention'])
            res.append(annotation)
    with open('my_entity_recall.json','w') as writer:
        writer.write(json.dumps(res,indent=1,ensure_ascii=False))             

if __name__ == '__main__':
    entity_recall('刘德华')
    #main()    

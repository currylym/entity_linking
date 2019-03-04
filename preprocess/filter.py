
'''
对数据进行格式整理和实体过滤
'''

import json

def filter(obj):
    #用来过滤机构、地名和人名实体
    maps = {
            '人物':'person',
            '历史人物':'person',
            '组织机构':'organization',
            '地点':'location',
            '地名':'location'
            }
    obj_concepts = list(obj['concept'].keys())
    need_concepts = list(maps.keys())
    if set(obj_concepts) & set(need_concepts):
        return obj 

def transform(obj):
    #对基本单元的格式进行变换
    obj1 = {}
    obj1['begin'] = obj['span'][0]
    obj1['end'] = obj['span'][1]
    obj1['mention'] = obj['mention']
    obj1['entity'] = obj['entity']
    obj1['concept'] = dict(obj['concept'])
    return obj1 

def main():
    data_path = 'el_testdata.json'
    rawdata = json.loads(open(data_path,'r').read())
    newdata = []
    for i in rawdata:
        annotation = [filter(transform(obj)) for obj in i['annotation'] if filter(transform(obj))]
        if annotation:
            newdata.append({'text':i['text'],
                            'annotation':annotation})
    with open('el_testdata_new.json','w') as f:
        f.write(json.dumps(newdata,indent=1,ensure_ascii=False))

if __name__ == '__main__':
    main()

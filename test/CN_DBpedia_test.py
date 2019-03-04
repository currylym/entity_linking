
import json
import sys
sys.path.append('..')

from config import config
from utils.utils import crawler
myconfig = config()
mycrawler = crawler(check_url='http://shuyantech.com/api/entitylinking/cutsegment?q=打球的李娜和唱歌的李娜不是同一个人')

def CN_DBpedia_entity_linking(sentence):
    url = 'http://shuyantech.com/api/entitylinking/cutsegment?q=%s' % sentence
    res = mycrawler.get_html(url)
    print(res)
    return json.loads(res)

def main():
    test_data = json.loads(open(myconfig.test_data_path).read())
    res = []
    for data in test_data:
        sentence = data['text']
        while True:
            res = CN_DBpedia_entity_linking(sentence)
            if res:
                data['CD-DBpedia result'] = res
                break
        res.append(data)
        #break
    with open('CN-DBpedia_result.json','w') as writer:
        writer.write(json.dumps(res,indent=1,ensure_ascii=False))

def test():
    res = json.loads(open('CN-DBpedia_result.json').read())
    count = 0
    right = 0
    for data in res:
        annotation = ['%d_%d_%s' % (i['begin'],i['end'],i['entity']) for i in data['annotation']]
        CN_DBpedia_result = ['%d_%d_%s' % (i[0][0],i[0][1],i[1]) for i in data['CD-DBpedia result']['entities']]
        if CN_DBpedia_result:
            count += len(annotation)
            right += len(set(annotation) & set(CN_DBpedia_result))
            print('annotation:',annotation)
            print('CN_DBpedia:',CN_DBpedia_result)
            print(count,right)
    precision = right/count
    print('precision : %.4f' % precision)

if __name__ == '__main__':
    #CN_DBpedia_entity_linking(sentence='打球的李娜和唱歌的李娜不是同一个人')
    #main()
    test()

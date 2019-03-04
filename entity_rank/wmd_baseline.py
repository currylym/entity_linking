
import sys
sys.path.append('..')
import json

from entity_recall.entity_recall import entity_recall
from doc_fe.doc_similarity import DocSimilarity 

def main(mention,context):
    DS = DocSimilarity()
    recall = entity_recall(mention)['baike_entry'] #暂时针对baike的召回结果
    if recall['main_entry']:
        entity_candidate = [recall['main_entry']] + recall['polysemantics']
    else:
        recall['baikesearch_entey']
    entity_score = []
    for entity in entity_candidate:
        if 'description' in entity:
            doc1 = entity['description']
        elif 'infobox' in entity:
            infobox = entity['infobox']
            doc1 = list(infobox.keys()) + list(infobox.values())
            doc1 = ','.join(doc2)
        doc_distance = DS.wmd_distance(doc1,context)
        entity_score.append((entity,doc_distance))
    entity_score = sorted(entity_score,key=lambda x:x[1])

    print('context : %s' % context)
    print('mention : %s' % mention)
    for entity,score in entity_score[:3]:
        print(json.dumps(entity,indent=1,ensure_ascii=False))
        print('score:%.4f' % score)

if __name__ == '__main__':
    #main(mention='刘德华',context='刘德华是忘情水的演唱者,他的妻子是朱丽倩，他们过着幸福美满的生活。')
    main(mention='小米',context='小米的用户忠诚度明显回升,但华为吸引力依旧是第一')
    main(mention='小米',context='我最喜欢的食物是小米')
    #main(mention='赵云',context='当时刘备亦依附在公孙瓒处，赵云得以与刘备深交。 [3]  公孙瓒与袁绍交战，派遣青州刺史田楷占据山东附近的土地，袁绍亦派数万大军前来争，公孙瓒便上表将刘备提升为别部司马，派刘备前去帮助田楷抵抗袁绍。赵云随刘备出征，为刘备掌管骑兵。')

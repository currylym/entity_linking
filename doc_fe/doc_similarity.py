
'''
计算文档的相似度（中文）
'''

import os
import numpy as np
from pyemd import emd

import sys
sys.path.append('..')
from doc_fe.doc_process import word_segment,_load_word_vec_lmdb 

def distance(v1,v2):
    dist = np.sum((v1-v2)**2)**(0.5)
    return dist

class DocSimilarity(object):

    def wmd_distance(self,doc1,doc2):
        
        vocabulary = list(set(word_segment(doc1)+word_segment(doc2)))
        v_len = len(vocabulary)
        #print(vocabulary)
        D_ = np.zeros((v_len,v_len),dtype='float')
        for i in range(v_len):
            for j in range(v_len):
                v1 = _load_word_vec_lmdb(vocabulary[i])
                v2 = _load_word_vec_lmdb(vocabulary[j])
                D_[i,j] = distance(v1,v2)
        D_ /= D_.max()  # just for comparison purposes
        #print(D_)
        def _doc_word_vec(doc):
            res = []
            wl = word_segment(doc)
            for word in vocabulary:
                res.append(wl.count(word))
            return np.array(res,dtype='double')
        v_1 = _doc_word_vec(doc1)
        v_2 = _doc_word_vec(doc2)
        #print(v_1,v_2)
        v_1 /= v_1.sum()
        v_2 /= v_2.sum()
        return emd(v_1, v_2, D_)        

if __name__ == '__main__':
    DS = DocSimilarity()
    score = DS.wmd_distance('鸣人和卡卡西','佐助是小樱的男朋友')
    print(score)

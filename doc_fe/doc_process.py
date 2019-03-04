
'''
对文档进行特征工程
'''
import jieba
MAIN_PATH = '../data/'
#若不注释掉下一行，则jieba会导入腾讯的额外字典来分词，这样效果好但是速度慢（待解决）
#jieba.load_userdict(MAIN_PATH+'tencent_word_small.txt')

import codecs
import numpy as np
from lmdb_embeddings.writer import LmdbEmbeddingsWriter
from lmdb_embeddings.reader import LmdbEmbeddingsReader
from lmdb_embeddings.exceptions import MissingWordError

#分句
def ss(doc):
    sents = doc.split('。')
    def _pre_process(sent):
        return sent.replace(' ','')
    return [_pre_process(sent) for sent in sents]

#分词
def word_segment(sentence):
    #去除停用词，加额外字典分词
    #print(sentence)
    if not sentence or not isinstance(sentence,str):
        return []
    seg_list = jieba.cut(sentence, cut_all=False)
    stopwords = open(MAIN_PATH+'chinese_stopwords.txt').read().split('\n')
    #print(seg_list)
    return [i for i in seg_list if i not in stopwords]

#从lmdb加载word embedding数据
def _load_word_vec_lmdb(word,path=MAIN_PATH+'/wv_lmdb',word_wv_dim=200):
    embeddings = LmdbEmbeddingsReader(path)
    try:
        vector = embeddings.get_word_vector(word)
        return vector
    except MissingWordError:
        #print('%s not in dict' % word)
        return np.zeros(word_wv_dim)

#加载词向量
def _load_char_vec(path):
    char_vec = {}
    with codecs.open(path, 'r', 'utf8') as reader:
        for line in reader:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            char_vec[parts[0]] = list(map(float, parts[1:]))
    char_vec[''] = [0.0] * len(char_vec[u'的'])
    return char_vec
fasttext_char = _load_char_vec(MAIN_PATH+'char.300.vec')

#pos
def pos(sent):
    return []

#ner，自己的ner api todo...
def ner(sent):
    return []

#针对单个sentence的主要embedding函数
def sentence_embedding(sentence,padding=20,char_pooling='max',word_wv_dim=200,
                       char_cv_dim=300):
    #输出维数：char_dim+word_dim,一般是500
    words = word_segment(sentence)
    #print(words)
    embedding = []
    for word in words:
        word_vec = _load_word_vec_lmdb(word)
        char_vecs = np.array([fasttext_char.get(i,np.zeros(char_cv_dim)) for i in word])
        #print(char_vecs.shape)
        if char_pooling == 'max':
            char_vec = np.max(char_vecs,axis=0)
        elif char_pooling == 'mean':
            char_vec = np.mean(char_vecs,axis=0)
        vec = np.hstack([word_vec,char_vec])
        embedding.append(vec.tolist())
    embedding = np.array(embedding)
    #print(embedding.shape)
    if not embedding.tolist():
        return np.zeros((padding,word_wv_dim+char_cv_dim),dtype='float')
    w_len = len(words)
    if  w_len < padding:
        embedding = np.vstack([embedding,np.zeros((padding-w_len,word_wv_dim+char_cv_dim),
                                                  dtype='float')])
    else:
        embedding = embedding[:padding,:]
    return embedding

def doc_fe(doc):
    #分句
    sents = ss(doc)
    res = []
    for sent in sents:
        ws_res = word_segment(sent)
        pos_res = pos(sent)
        ner_res = ner(sent)
        res.append({
                'text':sent,
                'ws':ws_res,
                'pos':pos_res,
                'ner':ner_res,
                'sentence_embedding':sentence_embedding(sent)})
    return res

if __name__ == '__main__':
    doc = '我爱北京天安门'
    print(doc_fe(doc))
    print(doc_fe('我来自湖北天门'))
    print(word_segment('鸣人和佐助是火影忍者中的角色'))
    print(doc_fe('鸣人和佐助是火影忍者中的角色'))

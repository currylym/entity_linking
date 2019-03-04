
import sys
sys.path.append('..')

from config import config

from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors
from gensim.test.utils import datapath

def main():
    mycogfig = config()
    wv_path_raw = mycogfig.embedding_path
    wv_from_text = KeyedVectors.load_word2vec_format(datapath(wv_path_raw), binary=False, unicode_errors='ignore', encoding='utf8')
    fname = get_tmpfile("../data/vectors.kv")
    wv_from_text.save(fname)

if __name__ == '__main__':
    main()

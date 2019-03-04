
import lmdb
import sys
sys.path.append('..')

from config import config
myconfig = config()

def create_lmdb(path='./lmdb_emb',map_size=21474836480):
    env = lmdb.open(path,map_size=map_size)
    return env

def insert(env, key, value):
    txn = env.begin(write=True)
    txn.put(str(key), value)
    txn.commit()

def main(path='./lmdb_emb'):
    env = create_lmdb(path=path)
    count = 0
    with open(myconfig.embedding_path) as f:
        for line in f:
            key,*value = line.replace('\n','').split(' ')
            if len(value) == 1:
                print('word num:%s' % key)
                continue
            value = ' '.join(value)
            print(key,value)
            insert(env, key, value)
            count += 1
            if count % 10000:print(count)
    env.close()

if __name__ == '__main__':
    main()

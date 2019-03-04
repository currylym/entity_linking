
'''
主要的路径配置
'''
class config(object):

    def __init__(self):
        main_path = r'/home/luyiming/entity_linking/'
        self.test_data_path = main_path + r'data/el_testdata_new.json' #实体链接的测试数据
        self.ip_path = main_path + r'utils/ip.txt' #本地的ip池列表
        self.embedding_path = main_path + 'data/Tencent_AILab_ChineseEmbedding.txt' #embedding路径

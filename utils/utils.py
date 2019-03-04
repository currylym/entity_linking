import os
import json
import random
import requests

import sys
sys.path.append('..')

#import自己的模块
from config import config
try:
    from utils.getIpList import GetIp
except:
    from getIpList import GetIp

myconfig = config()

class crawler(object):
    
    def __init__(self,check_url):
        self.ip_choose = -1 #当前选择的ip序号
        self.prob = 0.7 #每次输出当前选择ip序号的概率
        self.ip_list = [] #代理ip池
        self.check_url = check_url #用来测试代理ip是否有效的url
        self.flag = os.path.exists(myconfig.ip_path) #标记从本地读取ip的可行性
    
    #主方法
    def get_html(self,url):
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }
        ip_rand, proxies = self.get_proxie()
        print(proxies)
        try:
            request = requests.get(url=url, headers=header, proxies=proxies, timeout=3)
        except:
            request_status = 500
        else:
            request_status = request.status_code
        print(request_status)
        while request_status != 200:
            #从ip_list中去除无效的ip
            self.ip_list.pop(ip_rand)
            print('delete ip:',proxies)
            print('remain ip num:',len(self.ip_list))
            self.ip_choose = -1
            ip_rand, proxies = self.get_proxie()
            print(proxies)
            try:
                request = requests.get(url=url, headers=header, proxies=proxies, timeout=3)
            except:
                request_status = 500
            else:
                request_status = request.status_code
            print(request_status)
        self.ip_choose = ip_rand
        request.encoding = request.apparent_encoding
        return request.text
    
    #根据ip_list和ip_choose随机获得ip和端口。ip_choose==-1时随机抽取一个ip。
    def get_proxie(self):
        #为ip_list赋值
        if not self.ip_list:
            if self.flag:
                print('get ips from local file : %s' % myconfig.ip_path)
                self.ip_list = json.loads(open(myconfig.ip_path).read())
                self.flag = False
            else:
                self.get_new_ips()
        #从ip_list挑选一个ip
        ip_list = self.ip_list
        if random.random() < self.prob:
            random_number = self.ip_choose
        else:
            random_number = -1
        if random_number == -1:
            random_number = random.randint(0, len(ip_list) - 1)
        ip_info = ip_list[random_number]
        ip_url_next = '://' + ip_info['address'] + ':' + ip_info['port']
        proxies = {'http': 'http' + ip_url_next, 'https': 'https' + ip_url_next}
        return random_number, proxies

    #当ip_list为空时，重新获得ip_list
    def get_new_ips(self):
        print('prepare ip pool...')
        get_ip = GetIp(check_url=self.check_url)
        get_ip.main() 
        self.ip_list = json.loads(open(myconfig.ip_path).read())

if __name__ == '__main__':
    mycrawler = crawler(check_url='http://baike.baidu.com/item/%E5%91%A8%E6%9D%B0%E4%BC%A6')
    mycrawler.get_html("http://baike.baidu.com/item/张勇")

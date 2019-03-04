
from urllib import request
from lxml import etree
from urllib import parse

import sys
sys.path.append('..')
from utils.utils import crawler

class BaiduBaike(crawler):
    '''
    def __init__(self):
        pass
    '''

    #此处若注释掉这个get_html方法，则是使用代理ip池来进行html的获取，速度较慢；否则是直接用本机ip来获取html
    def get_html(self, url):
        #return get_html(url)
        return request.urlopen(url).read().decode('utf-8').replace('&nbsp;', '')
    
    def info_extract_baidu(self, word):  # 百度百科
        url = "http://baike.baidu.com/item/%s" % parse.quote(word)
        print(url)
        selector = etree.HTML(self.get_html(url))

        infos = {}
        infos['main_entry'] = self.extract_baidu(selector)
        infos['polysemantics'] = self.checkbaidu_polysemantic(selector)
        infos['baikesearch_entey'] = []
        for selector in self.baike_search(word):
            entry = self.extract_baidu(selector)
            if '公司' in entry['tags'] or '组织机构' in entry['tags'] or '社会' in entry['tags']:
                infos['baikesearch_entey'].append(entry)
            
        #infos = [info for info in info_list if len(info) > 2]
        return infos

    def extract_baidu(self, selector):
        info_data = {}
        if selector.xpath('//h2/text()'):
            info_data['current_semantic'] = selector.xpath('//h2/text()')[0].replace('    ', '').replace('（','').replace('）','')
        else:
            info_data['current_semantic'] = ''
        if info_data['current_semantic'] == '目录':
            info_data['current_semantic'] = ''

        info_data['tags'] = [item.replace('\n', '') for item in selector.xpath('//span[@class="taglist"]/text()')]
        info_data['tags'] = [i for i in info_data['tags'] if i]

        info_data['infobox'] = {}
        if selector.xpath("//div[starts-with(@class,'basic-info')]"):
            for li_result in selector.xpath("//div[starts-with(@class,'basic-info')]")[0].xpath('./dl'):
                attributes = [attribute.xpath('string(.)').replace('\n', '') for attribute in li_result.xpath('./dt')]
                values = [value.xpath('string(.)').replace('\n', '') for value in li_result.xpath('./dd')]
                for item in zip(attributes, values):
                    info_data['infobox'][item[0].replace('    ', '')] = item[1].replace('    ', '')
        
        info_data['description'] = ''.join(selector.xpath('//div[@class="lemma-summary"]/div/text()|//div[@class="lemma-summary"]/div/a/text()')).replace('\n','')    
        info_data['related_entry'] = list(set(selector.xpath('//div[@class="lemma-summary"]/div/a/text()')))
        return info_data

    def checkbaidu_polysemantic(self, selector):
        semantics = ['https://baike.baidu.com' + sem for sem in
                     selector.xpath("//ul[starts-with(@class,'polysemantList-wrapper')]/li/a/@href")]
        names = [name for name in selector.xpath("//ul[starts-with(@class,'polysemantList-wrapper')]/li/a/text()")]
        info_list = []
        if semantics:
            for item in zip(names, semantics):
                selector = etree.HTML(self.get_html(item[1]))
                info_data = self.extract_baidu(selector)
                info_data['current_semantic'] = item[0].replace('    ', '').replace('（','').replace('）','')
                if info_data:
                    info_list.append(info_data)
        return info_list
    
    def baike_search(self, word):
        url = 'https://baike.baidu.com/search/none?word=%s&pn=0&rn=10&enc=utf8' % parse.quote(word)
        selector = etree.HTML(self.get_html(url))
        entitys_url = [url for url in selector.xpath('//a[@class="result-title"]/@href') if 'https://baike.baidu.com/item/' in url]
        for url in entitys_url:
            yield etree.HTML(self.get_html(url))
        
if __name__ == '__main__':
    import json
    baidu = BaiduBaike(check_url="http://baike.baidu.com/item/李白")
    word = '周杰伦'
    #print(baidu.get_html("http://baike.baidu.com/item/%s" % parse.quote(word)))
    info = baidu.info_extract_baidu(word)
    print(json.dumps(info,indent=1,ensure_ascii=False))


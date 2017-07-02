# -*- coding: utf-8 -*-
__author__ = 'ZJM'
#######################################深度优先爬取全站#######################################
from scrapy.http import Request
from urllib import parse
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup
import re
from WuLiSpider.items import JsGoodsItem
class JdSpider(RedisSpider):
    def __init__(self, allowed_domains=None,model=None, *args, **kwargs):
        super(JdSpider, self).__init__(*args, **kwargs)

    name = "jd"
    allowed_domains = ["jd.com"]#######################################允许爬取的范围#######################################
    redis_key = 'jd:start_urls'
    #lpush jd:start_urls https://book.jd.com/
    # 收集所有404的url以及404页面数
    def parse(self, response):
        #解析网页
        soup = BeautifulSoup(response.text, "lxml")
        # 获取所有的链接
        nodes = soup.find_all("a")#######################################找到该网站的所有链接#######################################
        # 遍历链接节点
        for node in nodes:#######################################遍历所有链接#######################################
            #链接地址
            href = str(node.get('href'))
            #写规则
            if len(re.findall("item.jd.com\/\d+.html$",href)) > 0:#################################寻找符合条件的url 调整优先级下载并解析#######################################
                yield Request(url=parse.urljoin(response.url, href),callback=self.parse_detail, priority = 10, meta={"js":1})
            elif  href.find("jd.com") >= 0:#######################################不符合条件的url 下载并重复第一步第二步#######################################
                yield Request(url=parse.urljoin(response.url, href), callback=self.parse)
    def parse_detail(self, response):#######################################以下部分不用写进论文#######################################
        print("图书链接:"+response.url)
        soup = BeautifulSoup(response.body.decode(), "lxml")
        title = soup.title.text
        s = soup.find(id="jd-price")
        if s == None:
            s = soup.find_all("span", class_="p-price")[0]
        print(title+" 售价: "+s.text)

        pu = soup.find(id="popbox")
        if pu !=None and len(pu) >0:
            pu = pu.find_all("div", class_="mt")[0]
            store = pu.a.text
            storeUrl = pu.a.get("href")
        else:
            pu = soup.find("ul", class_="p-parameter-list")
            if pu == None:
                store=""
                storeUrl=""
            else:
                pu = pu.find(text=re.compile("品牌|店铺"))
                if pu == None:
                    store = "京东自营"
                    storeUrl = ""
                else:
                    pu = pu.parent
                    store = pu.a.text
                    storeUrl = pu.a.get("href")
        try:
            comments = soup.find_all("li", clstag=re.compile("shangpinpingjia"))[0]
            comments = comments.a.text
        except:
            comments = ""
        ##
        url = response.url
        id = re.split("/", url)
        id = id[len(id) - 1]
        id = re.split("\.", id)[0]
        jd_goods_item = JsGoodsItem()
        jd_goods_item["id"] = id
        jd_goods_item["name"] = title
        jd_goods_item["url"] = response.url
        jd_goods_item["price"] = str(s.text).replace("￥","")
        jd_goods_item["remark"] = ""
        jd_goods_item["store"] = store
        jd_goods_item["storeUrl"] = storeUrl
        jd_goods_item["comments"] = comments
        import datetime
        jd_goods_item["date"] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yield jd_goods_item
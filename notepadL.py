from ast import Num
from unicodedata import category
from numpy import append
import requests
from lxml import etree
from requests.exceptions import RequestException
import csv
from concurrent import futures
values = []
href2 = []

class BaseSpider(object):
    def __init__(self,url,multi_tag,worker=5):
        self.url = url
        # self.num = num
        self.multi_tag = multi_tag        
        self.worker_count = 5
        self.final_result = []

    def multi(self):
        if self.multi_tag == 'threading':
            pass
        if self.multi_tag == 'process':
            pass
        else:
            pass

    def get_page(self,url):
        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
                response.encoding='utf-8'
                return response.text
            return 0
        except RequestException:
            return 0

    def parse_page(self,text):
        global values
        html = etree.HTML(text)
        time = html.xpath("//table[@class='width-auto ']/tbody/tr/td[1]/text()")
        title = html.xpath("//table[@class='width-auto ']/tbody/tr/td[2]/a/text()")
        href = html.xpath("//table[@class='width-auto ']/tbody/tr/td[2]/a/@href")
        for i in href:
            global href2
            temp = 'https://wiki.ioin.in/'+ str(i)
            r=requests.get(url=temp,allow_redirects=False)
            href1 = r.headers['location']
            href2.append(href1)
        category = html.xpath("//table[@class='width-auto ']/tbody/tr/td[3]/a/text()")

        for i in range(len(title)):
            list = [time[i],title[i],href2[i],category[i]]
            values.append(list)
        return values

    def write_files(self,values):
        with open("result.csv","a+",newline='',encoding='utf8')as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(values)
    
    # def return_res(self):
    #     print("第"+str(self.get_page)+"页爬取结束")

    # def url_change(self,num):
    #     url = self.url+str(num)
    #     return url

if __name__=='__main__':
    
    webclawer = Spider("https://wiki.ioin.in/page-")
    with futures.ThreadPoolExecutor(max_workers=4) as pools:
        # task = pools.map(Spider,"https://wiki.ioin.in/page-",range(1,6))
        for num in range(1,6):
            f1 = pools.submit(webclawer.url_change,num)
            url = f1.result()

            f2 = pools.submit(webclawer.get_page,url)
            text = f2.result()

            f3 = pools.submit(webclawer.parse_page,text)
            values = f3.result()

            f4 = pools.submit(webclawer.write_files,values)
            f4.result()

            # text = webclawer.get_page(url)
            # values = webclawer.parse_page(text)
            # webclawer.write_files(values)

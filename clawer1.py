from unicodedata import category
from numpy import append
import requests
from lxml import etree
from requests.exceptions import RequestException
import csv
from concurrent import futures
values = []
href2 = []

def spider(offset):
    url = "https://wiki.ioin.in/page-"+str(offset)
    text = get_page(url)
    parse_one_page(text)
    write_to_files()
    print("第"+str(offset)+"页爬取结束")
    
def get_page(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            response.encoding='utf-8'
            return response.text
        return 0
    except RequestException:
        return 0

def parse_one_page(text):
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

def write_to_files():
    with open("result.csv","a+",newline='',encoding='utf8')as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(values)

if __name__=='__main__':
    
    with futures.ThreadPoolExecutor(max_workers=3) as pools:
        task = pools.map(spider,range(1,6))

    
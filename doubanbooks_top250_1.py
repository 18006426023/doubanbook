import requests
from lxml import etree
import time
import csv
import re
import codecs
from pyecharts import Bar
from multiprocessing import Pool
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}
BASE_URL = 'https://book.douban.com/top250?start={}'


def get_page(url):
    res = requests.get(url, headers=HEADERS)
    text = res.text
    html = etree.HTML(text)
    return html


def parse_page(url):
    res = requests.get(url, headers=HEADERS)
    text = res.text
    html = etree.HTML(text)
    titles = html.xpath("//div[@class='pl2']//a//@title")
    scores = html.xpath("//span[@class='rating_nums']/text()")
    # title_origins = html.xpath("//div[@class='pl2']//span/text()")
    book_details = html.xpath("//p[@class='pl']/text()")
    quotes = html.xpath("//p[@class='quote']//span/text()")
    links = html.xpath("//div[@class='pl2']//a//@href")
    d = []
    for title, score, book_detail, link in zip(titles, scores, book_details, links):
        # print(score)
        data = {}
        data['书名'] = title
        data['豆瓣评分'] = float(score[0:3])
        data['作者'] = book_detail.split('/')[0].strip()
        data['出版社'] = book_detail.split('/')[-3].strip()
        data['日期'] = book_detail.split('/')[-2].strip()
        data['价格'] = book_detail.split('/')[-1].strip()
        html1 = get_page(link)
        detail = html1.xpath("//div[@class='intro']//p/text()")
        # print(detail)
        data['内容简介'] = detail

        # data['典句'] = quote.strip()
        d.append(data)
    # print(d)
    return(d)


if __name__ == '__main__':
    urls = [BASE_URL.format(str(i*25)) for i in range(0, 1)]
    start_1 = time.time()
    for url in urls:
        books = parse_page(url)
    end_1 = time.time()
    print('串行爬虫耗时：', end_1 - start_1)

    start_2 = time.time()
    pool = Pool(processes=2)
    pool.map(parse_page, urls)
    end_2 = time.time()
    print('2进程爬虫耗时：', end_2 - start_2)

    start_3 = time.time()
    pool = Pool(processes=4)
    pool.map(parse_page, urls)
    end_3 = time.time()
    print('4进程爬虫耗时：', end_3 - start_3)



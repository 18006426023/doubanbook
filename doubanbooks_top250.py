import requests
from lxml import etree

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}
BASE_URL = 'https://book.douban.com/top250?start={}'


def get_page(url):
    res = requests.get(url, headers=HEADERS)
    text = res.text
    html = etree.HTML(text)
    return html


def parse_page(html):
    titles = html.xpath("//div[@class='pl2']//a//@title")#书名
    scores = html.xpath("//span[@class='rating_nums']/text()")#评分
    book_details = html.xpath("//p[@class='pl']/text()")#书籍详细信息
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
        print(detail)
        data['内容简介'] = detail
        d.append(data)
    return(d)


if __name__ == '__main__':
    urls = [BASE_URL.format(str(i*25)) for i in range(0, 10)]
    with open('douban_book_top250.txt', 'a', encoding='utf-8') as f:
        for url in urls:
            html = get_page(url)
            books = parse_page(html)

            for book in books:
                f.write('书名：' + str(book['书名']) + '\n')
                f.write('豆瓣评分：' + str(book['豆瓣评分']) + '\n')
                f.write('作者：' + str(book['作者']) + '\n')
                f.write('出版社：' + str(book['出版社']) + '\n')
                f.write('日期：' + str(book['日期']) + '\n')
                f.write('价格：' + str(book['价格']) + '\n')
                f.write('内容简介：' + str(book['内容简介']) + '\n')
                f.write('-'*100 + '\n')

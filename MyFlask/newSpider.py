import requests
from lxml import etree
import sqlite3
import chardet
connect = sqlite3.connect("mySqlite.db")
cursor = connect.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS MySqlite(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,url TEXT,img TEXT)")


class Spider(object):
    def __init__(self):
        self.login_url = "https://www.qianqianhua.com/meinvtupian/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        }
        self.html_obj = None
        self.number = 1

    def content(self):
        max_code = self.html_obj.xpath('//ul[@class="listpic_box"]')
        for code in max_code:
            url = code.xpath('//li[@class="grid"]/div[@class="img"]/a/@href')
            title = code.xpath('//div[@class="tit"]/a/text()')
            img = code.xpath('//div[@class="img"]/a/img/@data-original')
            for url1, title1, img1 in zip(url, title, img):
                # print(f'url:{url1}\ntitle:{title1}\nimg:{img1}')
                cursor.execute(f"INSERT INTO MySqlite(title,url,img) VALUES ('{title1}','{url1}','{img1}')")
                connect.commit()
            print("下载成功")

    def get_page(self):
        main_url = self.login_url
        html = requests.get(main_url, headers=self.headers).content.decode("UTF-8", "ignore")
        # 检查编码
        # Encoding = chardet.detect(html.content)['encoding']
        # print(Encoding)
        self.html_obj = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
        # print(type(self.html_obj))
        self.number += 1
        self.login_url = f'https://www.qianqianhua.com/meinvtupian/index_{self.number}.html'
        if self.number < 18:
            # 回调函数
            self.content()
            self.get_page()


if __name__ == '__main__':
    s = Spider()
    s.get_page()

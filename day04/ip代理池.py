import random

import MySQLdb
import requests
from lxml import etree


class Ip_pool():
    def __init__(self):
        self.limit=150
    def open_db(self):
         conn = MySQLdb.connect(
             host='localhost',
             port=3306,
             user='root',
             password='123456',
             db='spider',
             charset='utf8')
         return conn
    # 1.向代理池中存入ip
    def save_ip(self,ip,port,type):
        if self.check_ip(ip,port,type):
            conn = self.open_db()
            cur = conn.cursor()
            sql = 'insert into ip_pool values(%s,%s,%s)'
            cur.execute(sql,(ip,port,type))
            conn.commit()
    # 2.从代理池中取出IP
    def get_ip(self):
        conn = self.open_db()
        cur = conn.cursor()
        sql='select ip,port,type from ip_pool'
        cur.execute(sql)
        ips = cur.fetchall()
        ip = random.choice(ips)
        return {ip[2]:ip[0]+':'+ip[1]}
    # 3. 遍历数据库判断IP可用性(定时、定量)
    def check_allip(self):
        conn = self.open_db()
        cur = conn.cursor()
        sql = 'select ip,port,type from ip_pool'
        cur.execute(sql)
        ips = cur.fetchall()
        for i in ips:
            if not self.check_ip(i[0],i[1],i[2]):
                sql = 'delete from ip_pool where ip=%s'
                cur.execute(sql,(i[0],))
                conn.commit()
    # 4.检测某个ip是否可用
    def check_ip(self,ip,port,type):
        ips = {
            type:ip+":"+port
        }
        try:
            res = requests.get(url='http://www.httpbin.org/ip', proxies=ips, timeout=5).text
            print(ips)
            print(res)
        except:
            return False
        if ip in res:
            print('xxxxxxxxxx')
            return True
        return False
    # 5. 控制IP数量
    def count_ip(self):
        conn = self.open_db()
        cur = conn.cursor()
        sql = 'select * from ip_pool'
        ip_number = cur.execute(sql)

        if ip_number<self.limit:
            return True
        return False
    # 6. 爬取代理
    def crawl_ip(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        url = 'http://qinghuadaili.com/free/'
        page=1
        while self.count_ip():
            url1 = url + str(page) + '/'
            page+=1
            try:
                res = requests.get(url=url1,headers=headers).text
            except:
                continue
            ele = etree.HTML(res)
            ip = ele.xpath("/html/body/div/div/div/div[2]/table/tbody/tr/td[1]/text()")
            port = ele.xpath("/html/body/div/div/div/div[2]/table/tbody/tr/td[2]/text()")
            type = ele.xpath("/html/body/div/div/div/div[2]/table/tbody/tr/td[4]/text()")
            for i in range(len(ip)):
                self.save_ip(ip[i],port[i],type[i].lower())

if __name__ == '__main__':
        ippool = Ip_pool()
        # ippool.crawl_ip()
        ippool.check_allip()
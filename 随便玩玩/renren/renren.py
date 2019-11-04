import requests
import re
import MySQLdb
from lxml import etree
from 随便玩玩.renren.chaojiying import check_code
conn = MySQLdb.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password ='123456',
    db = 'spider',
    charset = 'utf8',
)
cur = conn.cursor()
cookies = {
    'Cookie': 'ick=ac623e26-f67d-4391-854d-c94cb69852b9;t=0c13c2c9a0965263fee4688b8c684ebb9;'
}

def insert_user(ele,id):
    print(id)
    nick = ele.xpath("//div[@class='cover-bg']/h1/text()")
    nick = nick[0].strip()
    school = ele.xpath("//li[@class='school']/span/text()")
    school = school[0] if school else '无'
    birthday = ele.xpath("//li[@class='birthday']/span[2]/text()")
    birthday = birthday[0][1:] if birthday else '无'
    hometown = ele.xpath("//li[@class='hometown']/text()")
    hometown = hometown[0] if hometown else '无'
    address = ele.xpath("//li[@class='address']/text()")
    address = address[0] if address else '无'
    sql = 'insert into user values(%s,%s,%s,%s,%s,%s)'
    cur.execute(sql,(id,nick,school,birthday,hometown,address))
    conn.commit()

def insert_url(ele):
    sql = 'insert into renren values(%s,%s)'
    url = ele.xpath("//div[@id='footprint-box']/ul/li/a/@namecard")  # 获取最近访问id
    url = ['http://www.renren.com/' + i + '/profile' for i in url]  # 拼接成正确网址
    url_firend = ele.xpath("//div[@class='share-friend']/ul/li/a/@namecard")  # 获取好友id
    url_firend = ['http://www.renren.com/' + i + '/profile' for i in url_firend]  # 拼接成正确网址
    urls = url + url_firend
    for url in urls:
        try:
            cur.execute(sql, (url, 0))
            conn.commit()
        except:
            pass
def engin():
    sql = 'select url from renren where state=0 limit 1'
    sql2 = 'update renren set state=1 where url = %s'
    res = cur.execute(sql)
    url = cur.fetchone()[0] if res == 1 else 'http://www.renren.com/880151247/profile'  # 设置开始第一个地址

    res = requests.get(url,cookies=cookies).text
    ele = etree.HTML(res)
    if ele.xpath("//title/text()")[0]=='人人网 - 验证码':
        print(ele.xpath("//title/text()")[0])
        img_url = ele.xpath("//div[@class='optional']/img/@src")[0]
        img = requests.get(img_url,cookies=cookies)
        with open('code.jpg','wb') as w:
            w.write(img.content)
        code = check_code(img.content).get('pic_str')
        check_url = 'http://www.renren.com/validateuser.do'
        data = {
            'id': '880792860',
            'icode': code,
            'submit': '继续浏览',
            'requestToken': '1314625249',
            '_rtk': '1a1c953b',
        }
        requests.post(check_url,data=data,cookies=cookies)
    else:
        cur.execute(sql2,(url,))
        conn.commit()
        print(ele.xpath("//title/text()")[0])
        id = re.findall('.*com/(.*)/.*',url)[0]
        insert_user(ele,id)  # 添加用户+
        insert_url(ele)      # 添加url

def run():
    while True:
        engin()

if __name__ == '__main__':
    run()
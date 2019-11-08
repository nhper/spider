import requests
import pymongo,random
conn = pymongo.MongoClient(host='localhost',port=27017)
mydb = conn['crawler']
myset = mydb['comment']
myset.create_index('content',unique=True)
# url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_417250909?offset='

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
}
def run():
    page=0
    while page<=81:
        print(page)
        url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_417250909?offset='+str(page*100)+"&limit=100"
        page+=1
        res = requests.get(url,headers=headers).json().get("comments")
        # print(res)
        # print(len(res))
        for data in res:
            content = data['content']
            item = {}
            item['content'] = content
            try:
                myset.insert_one(item)
            except Exception as f:
                print(f)
                print(item)
run()
# res = requests.get(url,headers=headers,proxies=random.choice(ips)).json()['comments']
# print(res)
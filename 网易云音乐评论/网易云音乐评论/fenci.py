import pymongo
import jieba
import wordcloud
conn = pymongo.MongoClient(host='localhost',port=27017)
mydb = conn['crawler']
myset = mydb['comment']

datas = myset.find()
x = ''
for data in datas:
    x+=(" ".join(jieba.lcut(data['content']))).replace('\n','')

w = wordcloud.WordCloud(font_path="FZSTK.TTF",scale=5)
w.generate(x)
w.to_file('x.jpg')

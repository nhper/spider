import time
import pymongo,random
from selenium import webdriver
conn = pymongo.MongoClient(host='localhost',port=27017)
mydb = conn['crawler']
myset = mydb['wyy_selenium']
myset.create_index('content',unique=True)
driver = webdriver.Chrome("./chromedriver.exe")
driver.get(url='https://music.163.com/song?id=417250909')
driver.implicitly_wait(5)
driver.switch_to.frame('contentFrame')
# button = driver.find_element_by_link_text("下一页")
# driver.execute_script("arguments[0].click();", button)
for i in range(402):
    button = driver.find_element_by_link_text("下一页")
    time.sleep(1)
    content = driver.find_elements_by_xpath("//div[@class='cmmts j-flag']/div/div[2]/div[1]")
    print(content)
    print(len(content))
    for i in content:
        c = {}
        c['content']=i.text
        print(i.text)
        try:
            # myset.insert(c)
            print('----------------------------------')
        except:
            print('重复')
    driver.execute_script("arguments[0].click();", button)
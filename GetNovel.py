from lxml import etree
import requests
from urllib import parse

def openUrl(url):
    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"}
    html = requests.get(url, headers=header)
    html.encoding = 'gbk'
    return html.text

def getTxt(html):
    tree = etree.HTML(html)
    a = tree.xpath('//div[@class="box_con"]/div')[2]
    txt = a.xpath('string(.)')
    return txt

def getNovel(html,name):
    tree = etree.HTML(html)
    lis = tree.xpath('//div[@id="list"]/dl/dd')
    flag = 0
    with open(name+'.txt','w',encoding='utf-8') as f:
        for li in lis:
            flag += 1
            if flag > 9:
                title = li.xpath('.//a/text()')[0]
                href = li.xpath('.//a/@href')[0]
                url = 'http://www.biquge.tv' + href
                content = getTxt(openUrl(url))
                f.write('\r\n'+title+'\r\n')
                f.write(content)
                print(flag-9)

def createGbkUrl(st):
    t = st.encode('gbk')
    b = parse.quote(t)
    url = 'http://www.biquge.tv/modules/article/search.php?searchkey=' + b
    return url

if __name__ == '__main__':
    name = input('输入书名:')
    url = createGbkUrl(name)
    html = openUrl(url)
    getNovel(html,name)

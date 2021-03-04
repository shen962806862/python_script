import requests, time
from PIL import Image
from io import BytesIO
import os,re

def openUrl(url):
    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"}
    html = requests.get(url, headers=header).text
    index1 = html.find('itemprop=\"image\"') + len('itemprop=\"image\" content=\"')
    index2 = html.find('\"', index1)
    cover = html[index1:index2]
    return cover

def getBVid(url):
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"}
    html = requests.get(url, headers=header, timeout=6).json()
    time.sleep(0.6)
    data = html['data']['list']['vlist']
    if data:
        all = []
        for info in data:
            title = info['title']
            bvid = info['bvid']
            aid = info['aid']
            tmp = []
            tmp.append(title)
            tmp.append(bvid)
            tmp.append(aid)
            all.append(tmp)
        return all
    else:
        return False

def getSingeAVid(BV):
    if BV.isdigit():
        url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid=' + BV
    else:
        if BV.startswith('http') or BV.startswith('bilibili'):
            link = BV
            pos = [m.start() for m in re.finditer('BV', link)][0]
            BV = link[pos:pos + 12]
        url = 'https://api.bilibili.com/x/web-interface/archive/stat?bvid=' + BV
    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"}
    html = requests.get(url, headers=header, timeout=6).json()
    data = html['data']['aid']
    return data

def getSingleCover(BV):
    if BV.isdigit():
        BV = getSingeAVid(BV)
    else:
        if BV.startswith('http') or BV.startswith('bilibili'):
            link = BV
            pos = [m.start() for m in re.finditer('BV', link)][0]
            BV = link[pos:pos+12]
    if not os.path.exists('./cover'):
        os.mkdir('./cover')
    path = openUrl('https://www.bilibili.com/video/' + BV)
    format = path[path.rfind('.'):]
    resp = requests.get(path)
    img = Image.open(BytesIO(resp.content))
    img.save('./cover/' + BV + format)

def downloadCover(UID):
    data = []
    for page in range(20):
        dt = getBVid('https://api.bilibili.com/x/space/arc/search?mid=' + str(UID) + '&ps=30&tid=0&pn=' + str(
            page + 1) + '&keyword=&order=pubdate&jsonp=jsonp')
        if dt:
            data.append(dt)
        else:
            break
    index = 0
    if not os.path.exists('./cover_' + str(UID)):
        os.mkdir('./cover_' + str(UID))
        f = open('./cover_' + str(UID) + '/data.txt', 'w', encoding='utf-8')
        for i in data:
            for j in i:
                index += 1
                path = openUrl('https://www.bilibili.com/video/' + j[1])
                format = path[path.rfind('.'):]
                resp = requests.get(path)
                img = Image.open(BytesIO(resp.content))
                img.save('./cover_' + str(UID) + '/' + str(index) + format)

                info = str(index) + format + ' : ' + j[0]
                f.write(info + '\r\n')
                print(info)
        print('total: ' + str(index))
        f.close()

if __name__ == "__main__":
    while True:
        mode = input("选择功能，获取：1.AV号 2.单个视频封面 3.up全部视频封面\n")
        UID = input('input message:')
        if mode == '1':
            print(getSingeAVid(UID))
        elif mode == '2':
            getSingleCover(UID)
        else:
            downloadCover(UID)
        print("----------Finished----------")

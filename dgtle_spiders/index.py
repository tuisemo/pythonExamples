# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
# import agents
import os
import time
import random

def getheaders():
    user_agent_list = ['Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
                       'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
                       'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
                       'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
                       'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']
    UserAgent = random.choice(user_agent_list)
    return UserAgent

# 抓取网址链接响应的数据
def catchPage(page):
    url = 'https://www.dgtle.com/article/getList/22'
    
    UserAgent = getheaders()
    headers = {
        'User-Agent':UserAgent,
    }
    params = {'page': page}
    try:
        res = requests.get(url, headers=headers, params=params)
    except:
        print(f'{url}已超时')
    else:
        jsonData = res.json()
        dataList = jsonData['data']['dataList']

        with ThreadPoolExecutor(max_workers=20) as t:  # 创建一个最大容纳数量为20的线程池
            for item in dataList:
                future = t.submit(catchDetailPage,item)
                future.add_done_callback(analysisData)
            t.shutdown(wait=True) # 关闭进程池的入口，等待池内任务运行结束
        # end = time.time()
        # print(f'共计耗时：{end - start}')

def catchDetailPage(item):
    id = item['id']
    url = f'https://www.dgtle.com/article-{id}-1.html'
    UserAgent = getheaders()
    headers = {
        'User-Agent':UserAgent,
    }
    try:
        res = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        print(f'{url}已超时')
    else:
        return {
            "res":res,
            "basePath":f'./_pics/{id}'
        }

def analysisData(future):
    data = future.result()
    res = data['res']
    basePath = data['basePath']
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(basePath)

    # # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(basePath)
        # print('创建成功')

    soup = BeautifulSoup(res.text,'html.parser')
    imgList = soup.select('figure > img')

    with ThreadPoolExecutor(max_workers=20) as task:
        for img in imgList:
            url = img.get('data-original')
            future = task.submit(savePic,(basePath,url))
        task.shutdown(wait=True) #关闭进程池的入口，等待池内任务运行结束

# 解析文档数据
def savePic(args):
    basePath,url=args
    try:
        res = requests.get(url)
    except:
        print(f'{url}已超时')
    else:
        fileName = os.path.basename(url)
        with open(f'{basePath}/{fileName}','wb') as f:
            f.write(res.content)
            print('已保存')



if __name__ == '__main__':
    start = time.time()
    with ThreadPoolExecutor(max_workers=10) as t:  # 创建一个最大容纳数量为10的线程池
        res = t.map(catchPage,[1,2,3])
        t.shutdown()
    end = time.time()
    print(f'共计耗时：{end - start}')
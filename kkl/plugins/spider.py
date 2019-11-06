# -*- coding:utf-8 -*-
from nonebot import on_command, CommandSession, permission as perm
import re
import requests
import jjcsearch
from random import randint
from google_translate import translate, ref_words
#import pandas as pd
#import numpy as np
#import json

@on_command('Rnews', aliases=('日服新闻','日服活动'), only_to_me=True)
async def Rnews(session: CommandSession):
    header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    url = 'https://priconne-redive.jp/news/'
    data = requests.get(url,headers = header)

    pattern_title = '<h4>(.*?)</h4>'#标题
    title = re.findall(pattern_title,data.text)

    pattern_link = '<a href="(.*?)">'#链接
    link0 = re.findall(pattern_link,data.text)
    link = []
    for i in range(len(link0)):
        if 'new' in link0[i]:
            link.append(link0[i])
    del(link[0],link[-1])

    pattern_time = '<time class="time">(.*?)</time>'#发布时间
    time = re.findall(pattern_time,data.text)

    msg0 = '已为骑士君查询最新{}条新闻：'.format(len(title))
    for i in range(len(title)):
        msg = (f'\n-----------------------------------------------\nNews{i+1}:\n标题:{title[i]}\n链接:{link[i]}\n时间:{time[i]}')
        msg0 += msg
    await session.send(message= msg0)

@on_command('Tnews', aliases=('台服新闻',), only_to_me=True)
async def Tnews(session: CommandSession):
    url = 'http://www.princessconnect.so-net.tw/news'
    header ={ 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    data = requests.get(url,headers = header)

    pattern_title = '<a href="/news/newsDetail/.*?">(.*?)</a>'#标题
    title = re.findall(pattern_title,data.text)

    pattern_link = '<a href="/news/(.*?)"'#链接
    link0 = re.findall(pattern_link,data.text)
    link = []
    for i in link0:
        link.append('http://www.princessconnect.so-net.tw/news/' + i)

    pattern_time = '(.*?)<span class=".*?">'#发布时间
    time0= re.findall(pattern_time,data.text)
    time = []
    for i in time0:
        time.append(i.strip())

    msg0 = '已为骑士君查询最新{}条新闻：'.format(len(title))
    for i in range(len(title)):
        msg = (f'\n-----------------------------------------------\nNews{i+1}:\n标题:{title[i]}\n链接:{link[i]}\n时间:{time[i]}')
        msg0 += msg
    await session.send(message= msg0)

@on_command('jjcsearch', aliases=('jjc查询','JJC查询','怎么拆','怎么解'), only_to_me=False)
async def jjcs(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
    #    msg0 = jjc.total(session.ctx['raw_message'])
        mark = jjcsearch.total(session.ctx['raw_message'],session.ctx['user_id'])
    #    await session.send('正在查询，请稍后...')
    #    msg='已为骑士君查到以下胜利队伍\n'
        if mark=='saved':
            await session.send('已为骑士君查到以下胜利队伍:\n[CQ:image,file=jjc/' + str(session.ctx['user_id']) + '.png]')
        else:
            await session.send(message= mark)
#    await session.send(msg0)

@on_command('ja_to_zh', aliases=('日语翻译',), only_to_me=False)
async def ja_to_zh(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
        msg=session.ctx['raw_message'][5:]
        re_msg = translate(msg[:4999], to='zh-CN', source='ja')
        if re_msg[0]!='' and re_msg[0]!=msg:
            await session.send(re_msg[0])

@on_command('ja_to_en', aliases=('英语翻译',), only_to_me=False)
async def ja_to_zh(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
        msg=session.ctx['raw_message'][5:]
        re_msg = translate(msg[:4999], to='zh-CN', source='en')
        if re_msg[0]!='':
            await session.send(re_msg[0])

@on_command('zh_to_ja', aliases=('翻译日语',), only_to_me=False)
async def ja_to_zh(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
        msg=session.ctx['raw_message'][5:]
        re_msg = translate(msg[:4999], to='ja', source='zh-CN')
        if re_msg[0]!='':
            await session.send(re_msg[0])

@on_command('zh_to_en', aliases=('翻译英语',), only_to_me=False)
async def ja_to_zh(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
        msg=session.ctx['raw_message'][5:]
        re_msg = translate(msg[:4999], to='en', source='zh-CN')
        if re_msg[0]!='':
            await session.send(re_msg[0])


@on_command('hbook', aliases=('本子查询','找本子'), only_to_me=False)
async def hbooks(session: CommandSession):
    if ' ' in session.ctx['raw_message']: 
        from_msg = session.ctx['raw_message'].split(' ',1)[1]#获取关键词
        from_type = session.ctx['message_type']
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        keyword={'show':'title,titleen,tags','keyboard':from_msg}
        responce = requests.post('https://zh.hcomics.club/search/',headers = header,data = keyword)
        if '没有搜索到相关的内容' in responce.text:
            n_msg='可可萝没有找到关键词[{}]相关的本子哦'.format(from_msg)
            await session.send(message=n_msg)
        else:
            p = '<a href="(.*?)" target="_blank" title="(.*?)">'
            data = re.findall(p,responce.text)
            n = len(data)
            if from_type == 'group':
                limit=3
            elif from_type == 'private':
                limit=10
            if n > limit:
                n = limit
            g_msg='[CQ:at,qq=' + str(session.ctx['user_id']) + ']\n已查询到{}本关键词为[{}]的本子：'.format(n,from_msg)
            p_msg='已查询到{}本关键词为[{}]的本子：'.format(n,from_msg)
            for i in range(n):
                msg0 = ('\n-----------------------------------------------\n本子链接：https://zh.hcomics.club%s \n本子标题：%s '%(data[i]))
                p_msg+=msg0
                g_msg+=msg0
            if from_type == 'group':
                await session.send(message=g_msg)
            elif from_type == 'private':
                await session.send(message=p_msg)
            else:
                pass

@on_command('hpics', aliases=('色图','来张色图','来份色图','我要色图','随机色图','不够色','色图呢','色图time'), only_to_me=False)
async def hpics(session: CommandSession):
#    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
#    img=requests.get('https://api.lolicon.app/setu/view.php',headers=header)
#    p='<img src=\\"(.*?)\\">'
#    link=re.findall(p,img.text)
#    await session.send(str(link[0]))
    await session.send(f'[CQ:image,file=色图库/色图{randint(1,50)}.png]')

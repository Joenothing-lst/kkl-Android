# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
root='C:\\Users\\Administrator\\Desktop\\kkl_responce.csv'
n = 1
a = pd.DataFrame(columns=('问','答','id'))
#存词条方法
def w(m,id):
    global a,n
    a = pd.read_csv(root,encoding='gbk',header=None,names=('问','答','id'))
    m=m.split('答')
    if '全局问' in m[0]:
        m[0]=m[0].replace('全局问','')
        a.loc[n] = (m[0],m[1],'1')
    else:
        m[0]=m[0].replace('问','')
        a.loc[n] = (m[0],m[1],str(id))
    n+=1
    a.to_csv(root,encoding='gbk')
    return '可可萝记住了~'
#判断关键词方法,将回答索引传入r()
def r(i):
    n = list(a['答'])[i]
    return n
#删除词条方法
def d(m,id):
    global a
    a = pd.read_csv(root,encoding='gbk',header=None,names=('问','答','id'))
    m=m.replace('删除词条','')
    if m in list(a['问']):
        if str(id) in list(a[a['问']==m]['id']):
            a.drop(index=a[a['问']==m].index,inplace=True)
            a.to_csv(root,encoding='gbk')
            return '已删除'
        else:
            if id == '1':
                return '这不是全局词条'
            else:
                return '你没有权限删除非本群词条或全局词条哦~ 主人的话请私聊~'
    else:
        return '可可萝不知道这个词哦~'
#备份词库方法
def s():
    a.to_csv(root,encoding='gbk')
    return '已保存！'
#读取词库方法
def rd():
    global a,n
    a = pd.read_csv(root,encoding='gbk',header=None,names=('问','答','id'))
    n = int(max(list(a.index.dropna())))+1
    return '已读取词库！'

# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import random as rd

gacya3 = {'杏奈':'[CQ:image,file=中二.png]',
        '真步':'[CQ:image,file=狐狸.png]',
        '璃乃':'[CQ:image,file=妹弓.png]',
        '初音':'[CQ:image,file=初音.png]',
        '霞':'[CQ:image,file=霞.png]',
        '伊緒':'[CQ:image,file=魅魔.png]',
        '咲戀':'[CQ:image,file=充电宝.png]',
        '望':'[CQ:image,file=偶像.png]',
        '妮諾':'[CQ:image,file=扇子.png]',
        '秋乃':'[CQ:image,file=哈哈剑.png]',
        '鏡華':'[CQ:image,file=xcw.png]',
        '智':'[CQ:image,file=tomo.png]',
        '真琴':'[CQ:image,file=狼.png]',
        '伊莉亞':'[CQ:image,file=伊利亚.png]',
        '純':'[CQ:image,file=黑骑.png]',
        '靜流':'[CQ:image,file=姐姐.png]',
        '莫妮卡':'[CQ:image,file=莫妮卡.png]',
        '流夏':'[CQ:image,file=流夏.png]',
        '吉塔':'[CQ:image,file=吉他.png]',
        '亞里莎':'[CQ:image,file=亚里莎.png]',
        '安':'[CQ:image,file=安.png]',
        '古蕾婭':'[CQ:image,file=龙姬.png]',
        '蕾姆':'[CQ:image,file=蕾姆.png]',
#        '爱蜜莉雅':'[CQ:image,file=爱蜜莉雅.png]',
        '空花(大江户)':'[CQ:image,file=江户抖m.png]',
        '妮諾(大江户)':'[CQ:image,file=江户扇子.png]'}

gacya2 = {'茉莉':'[CQ:image,file=跳跳虎.png]',
        '茜里':'[CQ:image,file=妹法.png]',
        '宮子':'[CQ:image,file=布丁.png]',
        '雪':'[CQ:image,file=镜子.png]',
        '七七香':'[CQ:image,file=七七香.png]',
        '美里':'[CQ:image,file=圣母.png]',
        '鈴奈':'[CQ:image,file=暴击弓.png]',
        '香織':'[CQ:image,file=狗.png]',
        '美美':'[CQ:image,file=兔子.png]',
        '綾音':'[CQ:image,file=熊锤.png]',
        '鈴':'[CQ:image,file=松鼠.png]',
        '惠理子':'[CQ:image,file=病娇.png]',
        '忍':'[CQ:image,file=忍.png]',
        '真陽':'[CQ:image,file=奶牛.png]',
        '栞':'[CQ:image,file=tp弓.png]',
        '千歌':'[CQ:image,file=千歌.png]',
        '空花':'[CQ:image,file=抖m.png]',
        '珠希':'[CQ:image,file=猫剑.png]',
        '美冬':'[CQ:image,file=子龙.png]',
        '深月':'[CQ:image,file=眼罩.png]',
        '紡希':'[CQ:image,file=裁缝.png]'}

gacya1 = {'日和':'[CQ:image,file=猫拳.png]',
        '優衣':'[CQ:image,file=优衣.png]',
        '怜':'[CQ:image,file=剑圣.png]',
        '禊':'[CQ:image,file=炸弹人.png]',
        '胡桃':'[CQ:image,file=铃铛.png]',
        '依里':'[CQ:image,file=姐法.png]',
        '鈴莓':'[CQ:image,file=女仆.png]',
        '優花梨':'[CQ:image,file=黄骑.png]',
        '碧':'[CQ:image,file=香菜.png]',
        '美咲':'[CQ:image,file=大眼.png]',
        '莉瑪':'[CQ:image,file=羊驼.png]',
        '步未':'[CQ:image,file=路人.png]'}

fesgacya = {'克莉絲提娜':'[CQ:image,file=克总.png]',
        '矛依未':'[CQ:image,file=511.png]',
        '杏奈':'[CQ:image,file=中二.png]',
        '真步':'[CQ:image,file=狐狸.png]',
        '璃乃':'[CQ:image,file=妹弓.png]',
        '初音':'[CQ:image,file=初音.png]',
        '霞':'[CQ:image,file=霞.png]',
        '伊緒':'[CQ:image,file=魅魔.png]',
        '咲戀':'[CQ:image,file=充电宝.png]',
        '望':'[CQ:image,file=偶像.png]',
        '妮諾':'[CQ:image,file=扇子.png]',
        '秋乃':'[CQ:image,file=哈哈剑.png]',
        '鏡華':'[CQ:image,file=xcw.png]',
        '智':'[CQ:image,file=tomo.png]',
        '真琴':'[CQ:image,file=狼.png]',
        '伊莉亞':'[CQ:image,file=伊利亚.png]',
        '純':'[CQ:image,file=黑骑.png]',
        '靜流':'[CQ:image,file=姐姐.png]',
        '莫妮卡':'[CQ:image,file=莫妮卡.png]',
        '流夏':'[CQ:image,file=流夏.png]',
        '吉塔':'[CQ:image,file=吉他.png]',
        '亞里莎':'[CQ:image,file=亚里莎.png]',
        '安':'[CQ:image,file=安.png]',
        '古蕾婭':'[CQ:image,file=龙姬.png]',
        '蕾姆':'[CQ:image,file=蕾姆.png]',
#        '爱蜜莉雅':'[CQ:image,file=爱蜜莉雅.png]',
        '空花(大江户)':'[CQ:image,file=江户抖m.png]',
        '妮諾(大江户)':'[CQ:image,file=江户扇子.png]'}

def gacya(up,fes):
    result = []
    msg = ''
    if fes == True:
        for n in range(10):
            i = rd.random()*1000
            if i >= 993:                     #up
                result.append(gacya3[up])
            elif i >= 950 and i < 993:       #3星
                result.append(rd.choice(list(fesgacya.values())))
            elif i >= 770 and i < 950:       #2星
                result.append(rd.choice(list(gacya2.values())))
            else :                           #1星
                result.append(rd.choice(list(gacya1.values())))
    else:
        for n in range(10):
            i = rd.random()*1000
            if i >= 993:                     #up
                result.append(gacya3[up])
            elif i >= 975 and i < 993:       #3星
                result.append(rd.choice(list(gacya3.values())))
            elif i >= 770 and i < 975:       #2星
                result.append(rd.choice(list(gacya2.values())))
            else :                           #1星
                result.append(rd.choice(list(gacya1.values())))
    for i in range(10):
        if i == 4:
            result[4] += '\n'
        msg += result[i]
    return msg
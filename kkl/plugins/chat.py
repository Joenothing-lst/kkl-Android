# -*- coding:utf-8 -*-
import nonebot
from nonebot import on_command, CommandSession, Message, permission as perm
from random import choice,randint
import os
import re
import wenda
import requests
from aiocqhttp.exceptions import ActionFailed
#from io import BytesIO
#from PIL import Image
from aip import AipOcr
#import pytesseract
import jieba
from collections import Counter


@on_command('send_group_list', aliases=('群信息',))
async def send_group_list(session: CommandSession):
    message_type=session.ctx['message_type'] 
    user_id=session.ctx['user_id']
    #判断发送的消息是私聊的，并且判断发送者的qq号码
    if message_type=='private' and user_id==912871833:
        #获取qq群的信息
        try:
    # your code
            group_list = await session.bot.get_group_list()
        except ActionFailed as e:
            print(e.retcode)
        msg='一共有{}个群：'.format(len(group_list))
        for group in group_list:
            msg+='\n-----------------\n'+'群名称:' + group['group_name'] + '\n' +'群号:' + str(group['group_id'])
        await session.bot.send_private_msg(user_id=912871833,message=msg)

@on_command('send_msg_info', aliases=('msg_info',), only_to_me=False)
async def ts(session: CommandSession):
    await session.send(message=str(session.ctx))

bot = nonebot.get_bot()

first=True
master = []
manager = []


@bot.on_message('group')
async def group_wenda_main(context):
    f_message = context['raw_message'].strip()
    f_group_id = context['group_id']
    f_user_id = context['user_id']
    global first

    if first:
        wenda.rd()
        print('\n可可萝启动，记忆装载完毕\n')
        first = False
    else:
        pass

    for i in range(len(list(wenda.a['问']))):
        if list(wenda.a['问'])[i] in f_message and '删除' not in f_message and '问' not in f_message and '答' not in f_message:
            if str(f_group_id)==list(wenda.a['id'])[i] or list(wenda.a['id'])[i]=='1':
                await bot.send_group_msg(group_id=f_group_id, message=wenda.r(i))

@bot.on_message('group')
async def group_wenda_update(context):
    f_message = context['raw_message'].strip()
    f_group_id = context['group_id']
    f_user_id = context['user_id']
    global manager,master
    if f_user_id in manager:
        if '删除词条' in f_message :
            await bot.send_group_msg(group_id=f_group_id, message=wenda.d(f_message,f_group_id))
        else:
            pass
        if '问' in f_message and '答' in f_message and '问答' not in f_message:
            if '全局' in f_message and f_message[2]=='问' and f_user_id in master:
                await bot.send_group_msg(group_id=f_group_id, message=wenda.w(f_message,'1'))
            elif '全局' not in f_message and f_message[0]=='问':
                await bot.send_group_msg(group_id=f_group_id, message=wenda.w(f_message,f_group_id))
            else: 
                pass
        if f_message == '保存词库':
            await bot.send_group_msg(group_id=f_group_id, message=wenda.s())
        if f_message == '读取词库':
            await bot.send_group_msg(group_id=f_group_id, message=wenda.rd())

@bot.on_message('private')
async def private_wenda_update(context):
    f_message = context['raw_message'].strip()
#    f_group_id = context['group_id']
    f_user_id = context['user_id']
    global manager,master
#    await bot.send_private_msg(user_id=f_user_id, message=context['message'])
    if f_user_id in manager:
        if '删除词条' in f_message :
            await bot.send_private_msg(user_id=f_user_id, message=wenda.d(f_message,'1'))
        else:
            pass
        if '问' in f_message and '答' in f_message and '问答' not in f_message:
            if '全局' in f_message and f_message[2]=='问' and f_user_id in master:
                await bot.send_private_msg(user_id=f_user_id, message=wenda.w(f_message,'1'))
            else: 
                pass
        if f_message == '保存词库':
            await bot.send_private_msg(user_id=f_user_id, message=wenda.s())
        if f_message == '读取词库':
            await bot.send_private_msg(user_id=f_user_id, message=wenda.rd())

@bot.on_message('group')
async def group_ban(context):
#    global manager,master
    f_message = context['raw_message'].strip()
    f_group_id = context['group_id']
    f_user_id = context['user_id']
    f_manager=[]
    try:
        group_memberinfo = await bot.get_group_member_list(group_id=f_group_id)
        for i in group_memberinfo:
            if i['role']=='owner' or i['role']=='admin':
                f_manager.append(i['user_id'])

        if '抽' in f_message and '奖' in f_message and '路' not in f_message:
            if f_user_id not in f_manager:
                little = randint(120,480)
                large = randint(10000,25000)
                if '大' in f_message or '带' in f_message:
                    await bot.set_group_ban( group_id=f_group_id, user_id=f_user_id, duration=large)
                else:
                    await bot.set_group_ban( group_id=f_group_id, user_id=f_user_id, duration=little)
            else:
                await bot.send_group_msg(group_id=f_group_id, message='权限狗无法参与(自裁吧')

        if '[CQ:at,qq=' in f_message and 'all' not in f_message and '一带一路' in f_message:
            p = 'CQ:at,qq=(\\d+)]'
            qq = int(re.search(p,f_message).group(1))
            if f_user_id not in f_manager and qq not in f_manager:
        #        print('get!!!')
                bantime = randint(120,480)
                await bot.set_group_ban( group_id=f_group_id, user_id=f_user_id, duration=bantime)
                await bot.set_group_ban( group_id=f_group_id, user_id=qq, duration=bantime + randint(-60,180))
                await bot.send_group_msg( group_id=f_group_id, message='恭喜[CQ:at,qq=' + str(f_user_id) + ']成功带动了[CQ:at,qq=' + str(qq) + ']的经济发展[CQ:image,file=C9F82E8E542E0C9345E85CF03D0D42C7.gif]')
            elif f_user_id not in f_manager and qq in f_manager:
                await bot.send_group_msg( group_id=f_group_id, message='[CQ:at,qq=' + str(f_user_id) + '] 你的行动失败了，没有符合帮扶政策的群员，你将独享')
                await bot.set_group_ban( group_id=f_group_id, user_id=f_user_id, duration=randint(120,480))
            elif f_user_id in f_manager:
                await bot.send_group_msg(group_id=f_group_id, message='权限狗无法参与(自裁吧')
            else:
                pass

        if '解除禁言' in f_message and '[CQ:at,qq=' in f_message and 'all' not in f_message:
            if f_user_id in f_manager:
                p = 'CQ:at,qq=(\\d+)]'
                qq = int(re.search(p,f_message).group(1))
                await bot.set_group_ban( group_id=f_group_id, user_id=qq, duration=0)
            else:
                await bot.send_group_msg( group_id=f_group_id, message='这是管理权限哦')

    #normar
        if '晚安' in f_message:
            if f_user_id in master:
                await bot.send_group_msg(group_id=f_group_id, message='[CQ:at,qq=' + str(f_user_id) + '] 晚安，主人~ mua~[CQ:image,file=TIM图片20190922214418_waifu2x_art_noise2_tta_1.png]')
            else :
                await bot.send_group_msg(group_id=f_group_id, message='[CQ:at,qq=' + str(f_user_id) + '] 晚安，骑士君~[CQ:image,file=TIM图片20190922214418_waifu2x_art_noise2_tta_1.png]')
        elif '送' in f_message and '我' in f_message:
            await bot.send_group_msg(group_id=f_group_id, message='[CQ:image,file=AEAEFF192D082E289F9859CE4424B2B0.jpg]')
        elif '妈' in f_message :
            f=True
            for i in ['狗','你','的','他','草','呀','查询']:
                if i in f_message:
                    f=False
            if f:
                await bot.send_group_msg(group_id=f_group_id, message='[CQ:at,qq=' + str(f_user_id) + ']？[CQ:image,file=EA6B4EF5F4759F7DAFEF70107A79F9A0.jpg]')
        else:
            pass
    except ActionFailed as e:
        print(e.retcode)

@on_command('unset_ban', aliases=('大赦天下','大赦天下！'), only_to_me=False)
async def unset_ban(session: CommandSession):
#    global manager,master
    f_group_id=session.ctx['group_id']
    f_manager=[]
    group_memberinfo = await bot.get_group_member_list(group_id=f_group_id)
    for i in group_memberinfo:
        if i['role']=='owner' or i['role']=='admin':
            f_manager.append(i['user_id'])
    if session.ctx['message_type'] == 'group' and session.ctx['user_id'] in manager:
#        group_memberinfo = await bot.get_group_member_list(group_id=f_group)
        if len(group_memberinfo) <= 60:
            memberlist = []
            for m in group_memberinfo:
#                memberlist.append(m['user_id'])
#            for q in memberlist:
                await bot.set_group_ban( group_id=f_group_id, user_id=m['user_id'], duration=0)

@on_command('send_all_group', aliases=('公告',), only_to_me=False)
async def send_all_group(session: CommandSession):
#    msg=session.ctx['raw_message'].replace('公告','')
    if session.ctx['user_id'] in master:
        group_list = await session.bot.get_group_list()
        for group in group_list:
            if group['group_id'] not in [574978085,604248997,1015614502,476328543,904757594,895673396]:
                await bot.send_group_msg( group_id=group['group_id'], message=session.ctx['raw_message'][3:])
        await session.send('推送完成')

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',}
#        'Content-Type':'application/x-www-form-urlencoded'}

APP_ID = '*******' # 刚才获取的 ID，下同
API_KEY = '**********************'
SECRECT_KEY = '**********************'
client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
@on_command('img_to_str', aliases=('识图取字','取字'), only_to_me=False)
async def i_t_s(session: CommandSession):
    p='\\[CQ\\:image\\,file\\=.*?\\,url\\=(.*?)\\]'
    url=re.findall(p,str(session.ctx['message']))
    img=requests.get(url[0],headers=header)
    bt=img.content
#    text = client.basicGeneral(bt)#              普通
    text = client.basicAccurate(bt)#             高精度
    msg=''
    try:
        for i in text['words_result']:
            msg+=i['words']+'\n'
        await session.send('[CQ:at,qq=' + str(session.ctx['user_id']) + ']可可萝识别出以下文本：\n' + msg)
    except:
        await session.send('可可萝没有识别出文字哦')

@on_command('str_to_words', aliases=('取词',), only_to_me=True)
async def s_t_w(session: CommandSession):
    f_message = session.ctx['raw_message'][3:]
#    f_group_id = session.ctx['group_id']
    f_user_id = session.ctx['user_id']
    slist = [x for x in jieba.cut(f_message) if len(x) >= 2 and x!='\n']
    a=Counter(slist).most_common(20)
    if f_user_id == 2802898563:
        msg='已为女朋友提取以下关键词：\n'
        for i,j in a:
            msg+=i+'  词频:'+str(j)+'\n'
        await session.send(msg)
    else:
        msg='已提取以下关键词：\n'
        for i,j in a:
            msg+=i+'  词频:'+str(j)+'\n'
        await session.send(msg)


#私聊上报字段
'''{'font': 93119112,
    'message': [{'type': 'text', 'data': {'text': 'tst'}}],
    'message_id': -7,
    'message_type': 'private',
    'post_type': 'message',
    'raw_message': 'tst',
    'self_id': 1094913531,
    'sender': {'age': 20,
               'nickname': '国服第一偶像鸽手',
               'sex': 'male', 'user_id': 912871833},
    'sub_type': 'friend',
    'time': 1570363714,
    'user_id': 912871833,
    'to_me': True}'''

#群聊上报字段
'''{'anonymous': None,
    'font': 108238048,
    'group_id': 770429221,
    'message': [{'type': 'text', 'data': {'text': 'tst'}}],
    'message_id': -7,
    'message_type': 'group',
    'post_type': 'message',
    'raw_message': 'tst',
    'self_id': 1094913531,
    'sender': {'age': 20,
               'area': '绍兴',
               'card': '',
               'level': '活跃',
               'nickname': '国服第一偶像鸽手',
               'role': 'owner',
               'sex': 'male',
               'title': '',
               'user_id': 912871833},
    'sub_type': 'normal',
    'time': 1570385622,
    'user_id': 912871833,
    'to_me': False}'''

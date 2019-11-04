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

@on_command('send_antang', aliases=('看看安堂','看看安堂姐','康康安堂','康康安堂姐','来张安堂','来张安堂姐','安堂姐','安堂','来点安堂','来点安堂姐'), only_to_me=False)
async def antang(session: CommandSession):
    filePath = 'C:\\Users\\Administrator\\Downloads\\CQP-xiaoi\\酷Q Pro\\data\\image\\antang\\'
    lst=os.listdir(filePath)
    await session.send(f'[CQ:image,file=antang/{choice(lst)}]')

bot = nonebot.get_bot()

first=True
master = [912871833,2802898563]
manager = [912871833,1160744937,1402871154,760071008,2802898563,2125593405,1773942923,837309855,289254329]


@bot.on_message('group')
async def group_wenda_main(context):
    f_message = context['raw_message'].strip()
    f_group_id = context['group_id']
    f_user_id = context['user_id']
    global first

    if first:
        wenda.rd()
        print('\n可可萝启动，记忆装载完毕\n')
        #await bot.send_private_msg(user_id=912871833,message='可可萝启动，记忆装载完毕')
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
#            elif '全局' not in f_message and f_message[0]=='问':
#                await bot.send_private_msg(user_id=f_user_id, message=wenda.w(f_message,f_user_id))
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
'''
    for i in group_memberinfo:
        if i['role']=='owner' or i['role']=='admin':
            f_manager.append(i['user_id'])

#    for i in context:
#        print(i,type(i))
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
'''
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
#pytesseract.pytesseract.tesseract_cmd = 'C://Program Files (x86)/Tesseract-OCR/tesseract.exe'
APP_ID = '17576714' # 刚才获取的 ID，下同
API_KEY = 'gwjDNjYzWsdGwHxsa8DyuAGP'
SECRECT_KEY = '5bqz3C16U4QknWGKHxRswWo3b7eMzGw8'
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


#    print(text)
#{'log_id': 3472477253040444149, 'words_result_num': 6, 'words_result': [{'words': '长相思'}, {'words': '【清】纳兰性德'}, {'words': '山一程,水一程。身向榆'}, {'words': '关那畔行,夜深千帐灯。'}, {'words': '风一更,雪一更。聒碎乡'}, {'words': '心梦不成,故园无此声。'}]}
#    text = pytesseract.image_to_string(Image.open(buf),lang='chi_sim')



'''import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C://Program Files (x86)/Tesseract-OCR/tesseract.exe'
text = pytesseract.image_to_string(Image.open('E://figures/other/poems.jpg'))

 INFO: Self: 1094913531, Message -7 from 912871833@[群:697475156]: [CQ:image,file=CCD54EA1D1D8BAEB718FC5F7162D1C5F.jpg,url=https://gchat.qpic.cn/gchatpic_new/912871833/779166649-2932650714-CCD54EA1D1D8BAEB718FC5F7162D1C5F/0?vuin=1094913531&amp;amp;term=2]
[2019-10-20 23:43:15,601 nonebot] DEBUG: Parsing command: [CQ:image,file=CCD54EA1D1D8BAEB718FC5F7162D1C5F.jpg,url=https://gchat.qpic.cn/gchatpic_new/912871833/779166649-2932650714-CCD54EA1D1D8BAEB718FC5F7162D1C5F/0?vuin=1094913531&amp;amp;term=2]
[2019-10-20 23:43:15,601 nonebot] DEBUG: Matched command start: (empty)
[2019-10-20 23:43:15,601 nonebot] DEBUG: Split command name: ('[CQ:image,file=CCD54EA1D1D8BAEB718FC5F7162D1C5F.jpg,url=https:', '', 'gchat.qpic.cn', 'gchatpic_new', '912871833', '779166649-2932650714-CCD54EA1D1D8BAEB718FC5F7162D1C5F', '0?vuin=1094913531&amp;amp;term=2]')
[2019-10-20 23:43:15,601 nonebot] DEBUG: Command ('[CQ:image,file=CCD54EA1D1D8BAEB718FC5F7162D1C5F.jpg,url=https:', '', 'gchat.qpic.cn', 'gchatpic_new', '912871833', '779166649-2932650714-CCD54EA1D1D8BAEB718FC5F7162D1C5F', '0?vuin=1094913531&amp;amp;term=2]') not found
[2019-10-20 23:43:15,601 nonebot] DEBUG: Not a known command, ignored
'''
'''
一共有26个群：
-----------------
群名称:战舰少女R官托Collection
群号:237681308
-----------------
群名称:心爱的pcr机器人
群号:342318398
-----------------
群名称:海未海未海
群号:367695743
-----------------
群名称:碧蓝迦勒底方舟抽象群
群号:427766169
-----------------
群名称:之江新中国成立70周年
群号:476328543
-----------------
群名称:19.10混& 周六守门！
群号:574978085
-----------------
群名称:三个小仙女
群号:604248997
-----------------
群名称:一会会战专用
群号:605611313
-----------------
群名称:公主连接-臭鼬之家
群号:642523293
-----------------
群名称:每天8杯水的少女前线
群号:671880082
-----------------
群名称:水龙敬棉纺种植采摘场
群号:681748595
-----------------
群名称:RE公主链接-小花特惠群
群号:697475156
-----------------
群名称:PPPerseus的公会群
群号:707850931
-----------------
群名称:fox—公主连接！Re：Dive
群号:710426430
-----------------
群名称:社会主义好⑨
群号:741160323
-----------------
群名称:影之诗娱乐群
群号:744299579
-----------------
群名称:可可萝测试
群号:770429221
-----------------
群名称:兰德索尔白玉楼支部
群号:779166649
-----------------
群名称:佐仓的可可萝和30264个
群号:784238535
-----------------
群名称:男娼起义
群号:819157037
-----------------
群名称:时雨时雨时
群号:857065659
-----------------
群名称:公主链接(天使降临到
群号:865452021
-----------------
群名称:沙雕视频翻译
群号:869225022
-----------------
群名称:憨批咸鱼皮卡丘团
群号:904757594
-----------------
群名称:兰德索尔炼铜协会
群号:985476303
-----------------
群名称:SNA夕阳老年大学
群号:1015614502'''


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
# -*- coding:utf-8 -*-
from nonebot import on_notice, NoticeSession

# 将函数注册为群成员增加通知处理器
@on_notice('group_increase')
async def increase(session: NoticeSession):
    # 发送欢迎消息
    q = str(session.ctx['user_id'])
    # 判断新成员是否是自己
    if q=='1094913531':               
        await session.send('在下是可可萝，今后请多指教呐')
    else:
        await session.send(f'欢迎新大佬[CQ:at,qq={q}][CQ:image,file=A445C5AC07B417FA054EBB67924562AB.gif]')

@on_notice('group_decrease')
async def decrease(session: NoticeSession):
    # 发送消息
    q = str(session.ctx['user_id'])
    m = str(session.ctx['operator_id'])
    if m==q:
        await session.send(f'{q} 跑了')

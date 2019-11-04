# -*- coding:utf-8 -*-
from datetime import datetime
import nonebot
import pytz
import Hpic
from aiocqhttp.exceptions import Error as CQHttpError

groups=[770429221,237681308,342318398,367695743,427766169,476328543,605611313,642523293,671880082,681748595,697475156,707850931,744299579,710426430,741160323,779166649,784238535,857065659,865452021,985476303]

@nonebot.scheduler.scheduled_job('cron', hour='14', minute='50', second='0', misfire_grace_time=60) # = UTC+8 1445
async def pcr_reminder():
    print('pcr_reminder start')
    msg = '背刺Time背刺Time背刺Time背刺Time背刺Time!!!'
    bot = nonebot.get_bot()
    for group in groups:
        try:
            await bot.send_group_msg(group_id=group, message=msg)
#            print(f'群{group} 投递成功')
        except nonebot.CQHttpError as e:
            print(e)
#            print(f'Error：群{group} 投递失败')


@nonebot.scheduler.scheduled_job('cron', hour='8', minute='0', second='0', misfire_grace_time=60) # = UTC+8 1445
async def alarm():
    print('alarm start')
    msg = '起床啦！！！'
    bot = nonebot.get_bot()
    for group in groups:
        try:
            await bot.send_group_msg(group_id=group, message=msg)
#            print(f'群{group} 投递成功')
        except nonebot.CQHttpError as e:
            print(e)
#            print(f'Error：群{group} 投递失败')


@nonebot.scheduler.scheduled_job('cron', hour='23', minute='0', second='0', misfire_grace_time=60) # = UTC+8 1445
async def need_sleep():
    print('alarm start')
    msg = '现在23点，皆无该精致睡眠了，期间可可萝无人维护，你们轻点(x'
    bot = nonebot.get_bot()
    for group in groups:
        try:
            await bot.send_group_msg(group_id=group, message=msg)
#            print(f'群{group} 投递成功')
        except nonebot.CQHttpError as e:
            print(e)
#            print(f'Error：群{group} 投递失败')

@nonebot.scheduler.scheduled_job('cron', hour='4', minute='0', second='0', misfire_grace_time=60) # = UTC+8 1445
async def hpic():
    try:
        await Hpic.update()
    except:
        pass



'''
@nonebot.scheduler.scheduled_job('interval', minutes=1,misfire_grace_time=10) # = UTC+8 1445
async def alarm_t():
    print('alarm test start')
    msg = 'test！！！'
    bot = nonebot.get_bot()
    for group in groups:
        try:
            await bot.send_group_msg(group_id=group, message=msg)
            print(f'群{group} 投递成功')
        except nonebot.CQHttpError as e:
            print(e)
            print(f'Error：群{group} 投递失败')'''
'''
@nonebot.scheduler.scheduled_job('cron', hour='*')
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        await bot.send_group_msg(group_id=672076603,
                                 message=f'现在{now.hour}点整啦！')
    except CQHttpError:
        pass
'''

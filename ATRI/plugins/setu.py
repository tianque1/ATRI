import os
import time
import json
import sqlite3
from random import choice, randint
from pathlib import Path
from datetime import datetime
from random import choice
import nonebot
from nonebot import on_command, CommandSession

import config # type: ignore
from ATRI.modules import response # type: ignore


bot = nonebot.get_bot()
master = config.MASTER()
apikey = bot.config.LOLICONAPI # type: ignore

URL = 'https://api.lolicon.app/setu/'

SETU_REPLY = """Title: {title}
Pid: {pid}
{setu}
---------------
Complete time:{time}s"""


def now_time():
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now


setu_type = 1
@on_command('setu', patterns = (r"来[点丶张份副个幅][涩色瑟][图圖]|[涩色瑟][图圖]来|[涩色瑟][图圖][gkd|GKD|搞快点]|[gkd|GKD|搞快点][涩色瑟][图圖]|[图圖]来|[我你她他它]想要[点丶张份副][涩色瑟][图圖]|我想要[1一][张份幅副个只][涩色瑟][图圖]|[我你她他它]想[看|look][涩涩|色色]的东西"), only_to_me = False)
async def setu(session: CommandSession):
    group = session.event.group_id
    user = session.event.user_id
    start = time.perf_counter()
    if 0 <= now_time() < 5.5:
        await session.send(
            choice(
                [
                    'zzzz......',
                    'zzzzzzzz......',
                    'zzz...好涩哦..zzz....',
                    '别...不要..zzz..那..zzz..',
                    '嘻嘻..zzz..呐~..zzzz..'
                ]
            )
        )
    else:
        with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
            data0 = json.load(f)
        with open(Path('.') / 'ATRI' / 'plugins' / 'switch' / 'switch.json', 'r') as f:
            data1 = json.load(f)

        if str(user) in data0.keys():
            pass
        else:
            if data1["setu"] == "on":
                res = randint(1,10)
                if 1 <= res < 9:
                    res = randint(1,4)
                    if 1 <= res < 3:
                        if setu_type == 1:
                            res = randint(1,4)
                            con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'setu' / 'nearR18.db')
                            cur = con.cursor()
                            msg = cur.execute('SELECT * FROM nearR18 ORDER BY RANDOM() limit 1;')
                        
                            if 1 <= res < 3:
                                for i in msg:
                                    pid = i[0]
                                    title = i[1]
                                    img = i[7]
                                    end = time.perf_counter()
                                    await session.send(
                                        SETU_REPLY.format(
                                        title = title,
                                        pid = pid,
                                        setu = img,
                                        time = round(end - start, 3)
                                        )
                                    )
                            elif res == 4:
                                for i in msg:
                                    pid = i[0]
                                    title = i[1]
                                    img = i[7]
                                    end = time.perf_counter()
                                    await session.send('我找到涩图了！但我发给主人了\nο(=•ω＜=)ρ⌒☆')
                                    await bot.send_private_msg( # type: ignore
                                        user_id = master,
                                        message = f"主人，从群{group}来的涩图！热乎着！\nTitle: {title}\nPid: {pid}\n{img}\nComplete time: {round(end - start, 3)}"
                                    )
                        
                        elif setu_type == 2:
                            res = randint(1,4)
                            await session.send('别急！正在找图！')
                            start = time.perf_counter()
                            values = {
                                "apikey": apikey,
                                "r18": "0",
                                "num": "1"
                            }

                            try:
                                dc = json.loads(response.request_api_params(URL, values))
                                title = dc["data"][0]["title"]
                                pid = dc["data"][0]["pid"]
                                setu = dc["data"][0]["url"] #b64.b64_str_img_url(dc["data"][0]["url"])
                            except:
                                await session.send('失败了失败了失败了失...')
                                return
                            if 1 <= res < 3:
                                end = time.perf_counter()
                                await session.send(
                                    SETU_REPLY.format(
                                    title = title,
                                    pid = pid,
                                    setu = dc["data"][0]["url"],
                                    time = round(end - start, 3)
                                    )
                                )
                            elif res == 4:
                                end = time.perf_counter()
                                await session.send('我找到涩图了！但我发给主人了\nο(=•ω＜=)ρ⌒☆')
                                await bot.send_private_msg( # type: ignore
                                    user_id = master,
                                    message = f"主人，从群{group}来的涩图！热乎着！\nTitle: {title}\nPid: {pid}\n{setu}\nComplete time: {round(end - start, 3)}"
                                )
                    elif res == 4:
                        img = choice(
                            [
                                'SP.jpg', 'SP1.jpg', 'SP2.jpg'
                            ]
                        )
                        img = Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}'
                        img = os.path.abspath(img)
                        await session.send(f'[CQ:image,file=file:///{img}]')
                
                elif res == 10:
                    img = choice(
                        [
                            'GDZ.png', 'SHZY1.jpg', 'SHZY2.jpg', 'SHZY3.jpg', 'SHZY4.jpg', 'SHZY5.jpg', 'SHZY6.jpg'
                        ]
                    )
                    img = Path('.') / 'ATRI' / 'data' / 'img' / 'niceIMG' / f'{img}'
                    img = os.path.abspath(img)
                    await session.send(f'[CQ:image,file=file:///{img}]')

            else:
                await session.send('该功能已被禁用...')


@on_command('change_setu_type', aliases = ['涩图导向'], only_to_me =False)
async def _(session: CommandSession):
    global setu_type
    if session.event.user_id == master:
        msg = session.event.raw_message.split(' ', 1)
        s_type = msg[1]
        
        if s_type == '数据库':
            setu_type = 1
        
        elif s_type == '接口':
            setu_type = 2
        
        else:
            pass
        
        await session.send('okay~~~~')

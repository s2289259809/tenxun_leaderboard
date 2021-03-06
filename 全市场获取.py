# coding=utf-8
import requests, re, time
import get_mysql
from multiprocessing import Pool, Manager, Process
import multiprocessing as mp
import random
import log


requests.packages.urllib3.disable_warnings()
logger = log.logger

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; vivo Y67A Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045008 Mobile Safari/537.36 V1_AND_SQ_8.3.3_1376_YYB_D QQ/8.3.3.4515 NetType/WIFI WebP/0.3.0 Pixel/720 StatusBarHeight/49 SimpleUISwitch/0 QQTheme/1000',
    # 'cookie':str(denglu)
    'cookie': 'ptcz=524226d2afe911330fbfb452ece92c88adaf537005227086da273eb7e9063cd5; pgv_pvi=2405019648; RK=8qQlllsT7n; pgv_pvid=6010152923; ts_refer=ui.ptlogin2.qq.com/; ts_uid=5448687400; uin=o0657110547; skey=@shjwX0QAr; p_uin=o0657110547; pt4_token=Zs-NE*oJJhRTQEmFDl3j-atzbKB0cp9T8fQiB3nAXvw_; p_skey=rN-gkfP8hZoufjX8eHT9nHUITiB5QRgqA6cQYFY1nX0_; pgv_info=ssid=s5485149412; ts_last=zb.vip.qq.com/v2/pages/itemDetail',
    'referer': 'https://zb.vip.qq.com/v2/pages/itemDetail?appid=2&itemid=10871&_nav_titleclr=000000&_nav_txtclr=000000',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
}
obj = get_mysql.SqlHelper()

'''链接数据库'''


def get_sql(id_tenxun, name, like, type, author):
    '''主题：1   3
       气泡：2
       名片：3   15
       挂件：4
       背景：8'''
    obj = get_mysql.SqlHelper()
    obj.modify('INSERT INTO tenxun_preview(tenxun_id,tenxun_name,likes,type,author) VALUES (%s,%s,%s,%s,%s)',
               [id_tenxun, name, like, type, author])
    obj.close()


def get_sql_update(id_tenxun, like):
    '''主题：1
       气泡：2'''
    obj = get_mysql.SqlHelper()
    print(id_tenxun, like)
    obj.modify('UPDATE tenxun_preview SET likes = %s WHERE tenxun_id = %s', [like, id_tenxun])
    obj.close()


'''遍历获取'''


def data_collection_bubble(mub_bubble):
    # 气泡：2
    error_bubble = 50
    # mub_bubble = 14583
    while True:
        if mub_bubble == 7200:
            print('气泡退出%s' % mub_bubble)
            break
        else:
            url = 'https://zb.vip.qq.com/v2/pages/itemDetail?appid=2&itemid=' + str(
                mub_bubble) + '&_nav_titleclr=000000&_nav_txtclr=000000'
            r = requests.get(url=url, headers=headers)
            r.encoding = 'utf-8'
            time.sleep(1)
            # print(mub_bubble)
            if '提供' in r.text:
                name = re.findall('<p class="name" data-v-4c6112a2>(.*)</p><span', r.text, re.S)[0]
                like = re.findall('likeCount":([0-9]*)', r.text, re.S)[0]
                author = re.findall('由(.*)提供', r.text, re.S)[0]
                logger.info('气泡,%s,%s,%s,id%s' % (name, like, author, mub_bubble))
                print('气泡,%s,%s,%s,id%s' % (name, like, author, mub_bubble))
                if author != '鹅真好看':
                    try:
                        # get_sql(mub_bubble, name, like,'2',author)
                        # print(mub_bubble, name, like, '2', author)
                        obj.modify(
                            'INSERT INTO tenxun_preview(tenxun_id,tenxun_name,likes,type,author) VALUES (%s,%s,%s,%s,%s)',
                            [mub_bubble, name, like, '2', author])
                        print('提交正常')
                    except:
                        try:
                            print(mub_bubble, like)
                            obj.modify('UPDATE tenxun_preview SET likes = %s WHERE tenxun_id = %s and type = 2',
                                       [like, mub_bubble])
                            print('更新正常')
                        except Exception as e:
                            print(e)

            else:
                logger.error('无数据气泡,%s' % mub_bubble)
                error_bubble += 1
                print('无数据')
            mub_bubble -= 1


def data_collection_theme(mub_theme):
    # 主题：1

    error_theme = 50
    # mub_bubble = 14583
    while True:
        if mub_theme == 1010000:
            print('主题退出%s' % mub_theme)
            break
        else:
            url = 'https://zb.vip.qq.com/v2/pages/itemDetail?appid=3&itemid=' + str(
                mub_theme) + '&_nav_titleclr=000000&_nav_txtclr=000000'
            r = requests.get(url=url, headers=headers)
            r.encoding = 'utf-8'
            time.sleep(1)
            # print(mub_theme)
            if '提供' in r.text:
                name = re.findall('<p class="name" data-v-4c6112a2>(.*)</p><span', r.text, re.S)[0]
                like = re.findall('likeCount":([0-9]*)', r.text, re.S)[0]
                author = re.findall('由(.*)提供', r.text, re.S)[0]

                # print(name,like,author)
                logger.info('主题,%s,%s,%s,id%s' % (name, like, author, mub_theme))
                print('主题,%s,%s,%s,id%s' % (name, like, author, mub_theme))
                if author != '鹅真好看' or '没有找到这个个性装扮' in r.text:
                    try:
                        obj.modify(
                            'INSERT INTO tenxun_preview(tenxun_id,tenxun_name,likes,type,author) VALUES (%s,%s,%s,%s,%s)',
                            [mub_theme, name, like, '1', author])
                        print('提交正常')
                    except:
                        obj.modify('UPDATE tenxun_preview SET likes = %s WHERE tenxun_id = %s and type = 1',
                                   [like, mub_theme])
                        print('更新正常')

            else:
                error_theme += 1
                logger.error('无数据主题,%s' % mub_theme)
                print('无数据')
            mub_theme -= 1


def data_collection_Pendant(mub_Pendant):
    # 挂件：4
    error_theme = 50
    # mub_bubble = 14583
    while True:
        if mub_Pendant == 5000:
            print('挂件退出%s' % mub_Pendant)
            break
        else:
            url = 'https://zb.vip.qq.com/v2/pages/itemDetail?appid=4&itemid=' + str(
                mub_Pendant) + '&_nav_titleclr=000000&_nav_txtclr=000000'
            r = requests.get(url=url, headers=headers)
            r.encoding = 'utf-8'
            # print(mub_Pendant)
            if '提供' in r.text:
                name = re.findall('<p class="name" data-v-4c6112a2>(.*)</p><span', r.text, re.S)[0]
                like = re.findall('likeCount":([0-9]*)', r.text, re.S)[0]
                author = re.findall('由(.*)提供', r.text, re.S)[0]

                # print(name,like,author)
                logger.info('挂件,%s,%s,%s,id%s' % (name, like, author, mub_Pendant))
                print('挂件,%s,%s,%s,id%s' % (name, like, author, mub_Pendant))
                if author != '鹅真好看':
                    try:
                        obj.modify(
                            'INSERT INTO tenxun_preview(tenxun_id,tenxun_name,likes,type,author) VALUES (%s,%s,%s,%s,%s)',
                            [mub_Pendant, name, like, '4', author])
                        print('提交正常')
                    except:
                        obj.modify('UPDATE tenxun_preview SET likes = %s WHERE tenxun_id = %s and type = 4',
                                   [like, mub_Pendant])
                        print('更新正常')

            else:
                error_theme += 1
                logger.error('无数据挂件,%s' % mub_Pendant)
                print('无数据')
            mub_Pendant -= 1


def data_collection_card(mub_card):
    # 名片：3
    error_theme = 50
    # mub_bubble = 14583
    while True:
        if mub_card == 5600:
            print('名片退出%s' % mub_card)
            break
        else:
            url = 'https://zb.vip.qq.com/v2/pages/itemDetail?appid=15&itemid=' + str(
                mub_card) + '&_nav_titleclr=000000&_nav_txtclr=000000'
            r = requests.get(url=url, headers=headers)
            r.encoding = 'utf-8'
            # print(mub_card)
            if '提供' in r.text:
                name = re.findall('<p class="name" data-v-4c6112a2>(.*)</p><span', r.text, re.S)[0]
                like = re.findall('likeCount":([0-9]*)', r.text, re.S)[0]
                author = re.findall('由(.*)提供', r.text, re.S)[0]
                # print(name,like,author)
                logger.info('名片,%s,%s,%s,id%s' % (name, like, author, mub_card))
                print('名片,%s,%s,%s,id%s' % (name, like, author, mub_card))
                if author != '鹅真好看':
                    try:
                        obj.modify(
                            'INSERT INTO tenxun_preview(tenxun_id,tenxun_name,likes,type,author) VALUES (%s,%s,%s,%s,%s)',
                            [mub_card, name, like, '3', author])
                        print('提交正常')
                    except:
                        obj.modify('UPDATE tenxun_preview SET likes = %s WHERE tenxun_id = %s and type = 3',
                                   [like, mub_card])
                        print('更新正常')

            else:
                error_theme += 1
                logger.error('无数据名片%s' % mub_card)
                print('无数据')
            mub_card -= 1


def start():
    #开启多线程
    theme = Process(target=data_collection_theme, args=(1031993,))
    # theme = Process(target=data_collection_theme, args=(1026433,))
    bubble = Process(target=data_collection_bubble, args=(43832,))
    # bubble = Process(target=data_collection_bubble, args=(30489,))
    Pendant = Process(target=data_collection_Pendant, args=(14885,))
    # Pendant = Process(target=data_collection_Pendant, args=(12479,))
    card = Process(target=data_collection_card, args=(11735,))
    # card = Process(target=data_collection_card, args=(9065,))
    theme.start()
    bubble.start()
    Pendant.start()
    card.start()
    print(theme.pid)
    print(bubble.pid)
    print(Pendant.pid)
    print(card.pid)
    bubble.join()
    theme.join()
    Pendant.join()
    card.join()
    obj.close()


if __name__ == '__main__':
    start()

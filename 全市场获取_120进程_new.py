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
    'cookie': 'ptcz=524226d2afe911330fbfb452ece92c88adaf537005227086da273eb7e9063cd5; pgv_pvi=2405019648; RK=8qQlllsT7n; pgv_pvid=6010152923; ts_refer=ui.ptlogin2.qq.com/; ts_uid=5448687400; uin=o0657110547; p_uin=o0657110547; pgv_info=ssid=s3571632907; skey=@UDeXHO4cV; pt4_token=h8lMVN8bxQL7CYWSNwwWVBrqbKCV2hUDQDXX9Hg7Wqc_; p_skey=T8Xrhn1p*ZeUfpq3UtREfn0PRWyhXRNuxzLr8JQJ-bk_; ts_last=zb.vip.qq.com/v2/pages/itemDetail',
    'referer': 'https://zb.vip.qq.com/v2/pages/itemDetail?appid=2&itemid=10871&_nav_titleclr=000000&_nav_txtclr=000000',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
}

'''遍历获取'''


def data_collection_bubble(mub_bubble):
    # 气泡：2
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
        # logger.info('气泡,%s,%s,%s,id%s' % (name, like, author, mub_bubble))
        print('气泡,%s,%s,%s,id%s' % (name, like, author, mub_bubble))
        if author != '鹅真好看' or '没有找到这个个性装扮' in r.text:
            sql_in(mub_bubble, name, like, '2', author)

def data_collection_theme(mub_theme):
    # 主题：1
    url = 'https://zb.vip.qq.com/v2/pages/itemDetail?appid=3&itemid=' + str(
        mub_theme) + '&_nav_titleclr=000000&_nav_txtclr=000000'
    r = requests.get(url=url, headers=headers)
    r.encoding = 'utf-8'
    time.sleep(1)
    # print(mub_theme)
    if '提供' in r.text or '没有找到这个个性装扮' in r.text:
        name = re.findall('<p class="name" data-v-4c6112a2>(.*)</p><span', r.text, re.S)[0]
        like = re.findall('likeCount":([0-9]*)', r.text, re.S)[0]
        author = re.findall('由(.*)提供', r.text, re.S)[0]

        # print(name,like,author)
        # logger.info('主题,%s,%s,%s,id%s' % (name, like, author, mub_theme))
        if author != '鹅真好看' or '没有找到这个个性装扮' in r.text:
            sql_in(mub_theme, name, like, '1', author)

def data_collection_Pendant(mub_Pendant):
    # 挂件：4
    url = 'https://zb.vip.qq.com/v2/pages/itemDetail?appid=4&itemid=' + str(
        mub_Pendant) + '&_nav_titleclr=000000&_nav_txtclr=000000'
    r = requests.get(url=url, headers=headers)
    r.encoding = 'utf-8'
    # print(mub_Pendant)
    if '提供' in r.text or '没有找到这个个性装扮' in r.text:
        name = re.findall('<p class="name" data-v-4c6112a2>(.*)</p><span', r.text, re.S)[0]
        like = re.findall('likeCount":([0-9]*)', r.text, re.S)[0]
        author = re.findall('由(.*)提供', r.text, re.S)[0]
        time.sleep(1)
        # print(name,like,author)
        # logger.info('挂件,%s,%s,%s,id%s' % (name, like, author, mub_Pendant))
        if author != '鹅真好看':
            sql_in(mub_Pendant, name, like, '4', author)


def data_collection_card(mub_card):
    # 名片：3
    url = 'https://zb.vip.qq.com/v2/pages/itemDetail?appid=15&itemid=' + str(
        mub_card) + '&_nav_titleclr=000000&_nav_txtclr=000000'
    r = requests.get(url=url, headers=headers)
    r.encoding = 'utf-8'
    time.sleep(1)
    # print(mub_card)
    if '鹅' in r.text or '没有找到这个个性装扮' in r.text:
        name = re.findall('{"appId":[0-9],"itemId":[0-9]*,"name":"(.*)","feeType":[0-9],"image"', r.text, re.S)[0]
        like = re.findall('likeCount":([0-9]*)', r.text, re.S)[0]
        author = re.findall('由(.*)提供', r.text, re.S)[0]
        # print(name,like,author)
        # logger.info('名片,%s,%s,%s,id%s' % (name, like, author, mub_card))
        # print('名片,%s,%s,%s,id%s' % (name, like, author, mub_card))
        if author != '鹅真好看':
            sql_in(mub_card, name, like, '3', author)


def sql_in(mub, name, like, nub, author):
    obj = get_mysql.SqlHelper()
    if nub == '3':
        print('名片,%s,%s,%s,id%s' % (name, like, author, mub))
    if nub == '4':
        print('挂件,%s,%s,%s,id%s' % (name, like, author, mub))
    if nub == '1':
        print('主题,%s,%s,%s,id%s' % (name, like, author, mub))
    if nub == '2':
        print('气泡,%s,%s,%s,id%s' % (name, like, author, mub))
    try:
        obj.modify(
            'INSERT INTO tenxun_preview(tenxun_id,tenxun_name,likes,type,author) VALUES (%s,%s,%s,%s,%s)',
            [mub, name, like, nub, author])
        print('提交正常')
        logger.info('类型：%s,%s,%s,%s,id%s' % (nub,name, like, author, nub))
    except Exception as e:
        print(e)
        obj.modify('UPDATE tenxun_preview SET likes = %s WHERE tenxun_id = %s and type = 3',
                   [like, mub])
        print('更新正常')
        logger.error('类型：%s,%s,%s,%s,id%s' % (nub,name, like, author, nub))
    obj.close()

def list_sql():
    obj = get_mysql.SqlHelper()
    obj.multiple_modify()
    obj.close()

def process_start_theme(end_nub):
    pool = Pool(30)
    # for i in range(1010000, int(end_nub),-1):
    for i in range(int(end_nub), 1010000,-1):
        # 使用异步多进程的方式，启动子进程，并将功能函数和参数传入.
        # 注意: 这里的 args 必须传参数列表，就算是一个参数，也得写逗号结尾。
        # pool.apply_async(tenxun.uesr_txt, args=(user_name, passwd,), callback=alterUser)
        pool.apply_async(data_collection_theme, args=(i,))
        time.sleep(random.uniform(0.1, 0.5))
    pool.close()
    pool.join()  # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
    print('end')
def process_start_bubble(end_nub):
    pool = Pool(30)
    # for i in range(7200, int(end_nub),-1):
    for i in range(int(end_nub), 7200,-1):
        # 使用异步多进程的方式，启动子进程，并将功能函数和参数传入.
        # 注意: 这里的 args 必须传参数列表，就算是一个参数，也得写逗号结尾。
        # pool.apply_async(tenxun.uesr_txt, args=(user_name, passwd,), callback=alterUser)
        pool.apply_async(data_collection_bubble, args=(i,))
        time.sleep(random.uniform(0.1, 0.5))
    pool.close()
    pool.join()  # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
    print('end')
def process_start_Pendant(end_nub):
    pool = Pool(30)
    for i in range(int(end_nub), 5000,-1):
    # for i in range(5000, int(end_nub),-1):
        # 使用异步多进程的方式，启动子进程，并将功能函数和参数传入.
        # 注意: 这里的 args 必须传参数列表，就算是一个参数，也得写逗号结尾。
        # pool.apply_async(tenxun.uesr_txt, args=(user_name, passwd,), callback=alterUser)
        pool.apply_async(data_collection_Pendant, args=(i,))
        time.sleep(random.uniform(0.1, 0.5))
    pool.close()
    pool.join()  # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
    print('end')
def process_start_card(end_nub):
    pool = Pool(30)
    for i in range(int(end_nub), 5600,-1):
    # for i in range(5600, int(end_nub),-1):
        # 使用异步多进程的方式，启动子进程，并将功能函数和参数传入.
        # 注意: 这里的 args 必须传参数列表，就算是一个参数，也得写逗号结尾。
        # pool.apply_async(tenxun.uesr_txt, args=(user_name, passwd,), callback=alterUser)
        pool.apply_async(data_collection_card, args=(i,))
        time.sleep(random.uniform(0.1, 0.5))
    pool.close()
    pool.join()  # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
    print('end')


if __name__ == '__main__':
    # 开启多线程
    theme = Process(target=process_start_theme, args=(1036570,))
    # theme = Process(target=data_collection_theme, args=(1026433,))
    bubble = Process(target=process_start_bubble, args=(49656,))
    # bubble = Process(target=data_collection_bubble, args=(30489,))
    Pendant = Process(target=process_start_Pendant, args=(18863,))
    # Pendant = Process(target=data_collection_Pendant, args=(12479,))
    card = Process(target=process_start_card, args=(13055,))
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
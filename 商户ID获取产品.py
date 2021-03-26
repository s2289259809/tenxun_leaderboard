import get_mysql
import requests,re,datetime,json,time,random
from multiprocessing import Pool, Manager, Process

def Headers(cookies):
    headers = {
        'authority': 'zb.vip.qq.com',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; vivo NEX S Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045512 Mobile Safari/537.36 V1_AND_SQ_8.5.0_1596_YYB_D QQ/8.5.0.5025 NetType/WIFI WebP/0.3.0 Pixel/1080 StatusBarHeight/84 SimpleUISwitch/0 QQTheme/1000 InMagicWin/0',
        'content-type': 'application/json',
        'origin': 'https://zb.vip.qq.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://zb.vip.qq.com/v2/pages/beautyMall?supplyerid=1337856035',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cookie': str(cookies)
    }
    return headers

def Get_Business_Id():
    obj = get_mysql.SqlHelper()
    author_name = obj.get_list('SELECT author FROM `tenxun_preview` GROUP BY author', [])
    for i in author_name:
        print(i['author'])
        tenxun_nub = obj.get_one("SELECT tenxun_id,type FROM `tenxun_preview` WHERE author = %s", [i['author'], ])
        print(tenxun_nub)
        try:
            product_url = 'https://zb.vip.qq.com/v2/pages/itemDetail?appid=%s&itemid=%s&_nav_titleclr=000000&_nav_txtclr=000000' % (
            tenxun_nub['type'], tenxun_nub['tenxun_id'])
            product_re = requests.get(url=product_url, headers=Headers)
            tenxun_business_id = re.findall('productId":([0-9]*)', product_re.text, re.S)[0]
            tenxun_business_name = re.findall('ata-v-4c6112a2>由(.*)提供&gt;</span></p><', product_re.text, re.S)[0]
            try:
                obj.modify('INSERT INTO tenxun_business(tenxun_business_id,tenxun_business_name) VALUES(%s,%s)',
                           [tenxun_business_id, tenxun_business_name])
            except Exception as e:
                print(e)
            print(tenxun_business_id, tenxun_business_name)
            print('--------------------------------------------------------')
        except Exception as e:
            print(e)
    obj.close()

def Updata_time(skey,supplyerid,cookies):
    print(skey,supplyerid)
    url = "https://zb.vip.qq.com/trpc/cgi?daid=18&g_tk=291128172"
    for i in range(0,3):
        time.sleep(1)
        payload = "{\"namespace\":\"beautyMall\",\"cmd\":\"SupplyerInfo\",\"data\":{\"stlogin\":{\"ikeytype\":1,\"iopplat\":3,\"uin\":1542183954,\"sclientip\":\"\",\"skey\":\"@%s\"},\"supplyerid\":%s,\"nextID\":%s,\"Pagesize\":20}}"%(skey,supplyerid,i*20)
        resp = requests.post(url=url,headers=Headers(cookies), data=payload)
        # print(resp.text)
        error = 0
        while True:
            if error >= 5:
                break
            try:
                b = json.loads(str(resp.text))
                # print(b['data'])
                author = b['data']['supplyername']
            # print('-------------------------------------------------')
                for index,i in enumerate(b['data']['rpt_openitem']):
                    print(index)
                    product_url = 'https://zb.vip.qq.com/v2/pages/itemDetail?appid=%s&itemid=%s&_nav_titleclr=000000&_nav_txtclr=000000' % (
                        i['appid'], i['itemid'])
                    product = requests.get(url=product_url, headers=Headers(cookies)).text
                    # name = re.findall('{"appId":[0-9],"itemId":[0-9]*,"name":"(.*)","feeType":[0-9],"image"', product, re.S)[0]

                    try:
                        likes = i['likecnt']
                    except:
                        likes = 0
                    sql_in(i['itemid'], Get_Name(product), likes, i['appid'], get_mysql.Time_Stamp(i['onlinetime']), author)
                break
            except Exception as e:
                error+=1
                print('错误%s'%e)

def sql_in(mub, name, like, nub,date, author):
    obj = get_mysql.SqlHelper()
    if nub == 15:
        print('名片,%s,%s,%s,id%s,时间%s' % (name, like, author, mub,date))
    if nub == 4:
        print('挂件,%s,%s,%s,id%s,时间%s' % (name, like, author, mub,date))
    if nub == 3:
        print('主题,%s,%s,%s,id%s,时间%s' % (name, like, author, mub,date))
    if nub == 2:
        print('气泡,%s,%s,%s,id%s,时间%s' % (name, like, author, mub,date))
    if nub == 23:
        print('头像,%s,%s,%s,id%s,时间%s' % (name, like, author, mub,date))
    try:
        obj.modify(
            'INSERT INTO tenxun_preview(tenxun_id,tenxun_name,likes,type,date ,author) VALUES (%s,%s,%s,%s,%s,%s)',
            [mub,name, like, nub,date, author])
        print('提交正常')
    except Exception as e:
        print(e)
        print(date)
        obj.modify('UPDATE tenxun_preview SET likes = %s , date = %s,tenxun_name = %s WHERE tenxun_id = %s and type = %s',
                   [like,date,name, mub,nub])
        print('更新正常')
    obj.close()

def Get_Name(txt):
    # print(txt)
    name_json = re.findall('<script>window.__INITIAL_ASYNCDATA__=(.*)</script>', txt, re.S)[0]
    # print(name_json)
    b = json.loads(str(name_json))
    return b['itemInfo']['name']

if __name__ == '__main__':
    # Updata_time('tb7CWyXq8', '1111236025')

    pool = Pool(3)
    obj = get_mysql.SqlHelper()
    aa = obj.get_list('SELECT * FROM `tenxun_business`',[])
    for a in aa:
        Headers(
        # print(a['tenxun_business_id'])
        pool.apply_async(Updata_time,args=('rJeBU2d25',a['tenxun_business_id'],'ptcz=524226d2afe911330fbfb452ece92c88adaf537005227086da273eb7e9063cd5; pgv_pvi=2405019648; RK=8qQlllsT7n; ts_refer=ui.ptlogin2.qq.com/; pgv_pvid=6010152923; ts_uid=5448687400; uin=o1542183954; skey=@rJeBU2d25; p_uin=o1542183954; pt4_token=dPYK2iFMSny9ZtAOUjLuh6fZlyZjqQqY7vcoK0Omv5g_; p_skey=3DUa51n*bcRFeY84AE-YU1u8QG0g7LAIvLlgEUez1Qk_; pgv_info=ssid=s9152060960; ts_last=zb.vip.qq.com/v2/pages/beautyMall',)))
        time.sleep(random.uniform(0.1, 0.5))
    obj.close()
    pool.close()
    pool.join()  # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
    print('end')
    # print(get_mysql.Time_Stamp(1592207153))
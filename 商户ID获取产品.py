import get_mysql
import requests,re,datetime,json

def headers(cookies):
    global headers
    headers = {
        'authority': 'zb.vip.qq.com',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; vivo NEX S Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045512 Mobile Safari/537.36 V1_AND_SQ_8.5.0_1596_YYB_D QQ/8.5.0.5025 NetType/WIFI WebP/0.3.0 Pixel/1080 StatusBarHeight/84 SimpleUISwitch/0 QQTheme/1000 InMagicWin/0',
        'content-type': 'application/json',
        'origin': 'https://zb.vip.qq.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://zb.vip.qq.com/v2/pages/beautyMall?supplyerid=1110633869',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cookie': str(cookies)
    }

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
            product_re = requests.get(url=product_url, headers=headers)
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

def Updata_time(skey,supplyerid):
    print(supplyerid)
    url = "https://zb.vip.qq.com/trpc/cgi?daid=18&g_tk=1971637356"
    for i in range(0,20):
        payload = "{\"namespace\":\"beautyMall\",\"cmd\":\"SupplyerInfo\",\"data\":{\"stlogin\":{\"ikeytype\":1,\"iopplat\":3,\"uin\":1542183954,\"sclientip\":\"\",\"skey\":\"@%s\"},\"supplyerid\":%s,\"nextID\":%s,\"Pagesize\":20}}"%(skey,supplyerid,i*20)
        resp = requests.request("POST", url, headers=headers, data=payload.encode())
        # print(resp.text)
        try:
            b = json.loads(str(resp.text))
            # print(b['data'])
            author = b['data']['supplyername']
            # print('-------------------------------------------------')
            for i in b['data']['rpt_openitem']:
                product_url = 'https://zb.vip.qq.com/v2/pages/itemDetail?appid=%s&itemid=%s&_nav_titleclr=000000&_nav_txtclr=000000' % (
                    i['appid'], i['itemid'])
                product = requests.get(url=product_url, headers=headers).text
                name = re.findall('{"appId":[0-9],"itemId":[0-9]*,"name":"(.*)","feeType":[0-9],"image"', product, re.S)[0]
                sql_in(i['itemid'], name, i['likecnt'], i['appid'], get_mysql.Time_Stamp(i['onlinetime']), author)
        except Exception as e:
            print('错误%s'%e)

def sql_in(mub, name, like, nub,date, author):
    obj = get_mysql.SqlHelper()
    if nub == 3:
        print('名片,%s,%s,%s,id%s,时间%s' % (name, like, author, mub,date))
    if nub == 4:
        print('挂件,%s,%s,%s,id%s,时间%s' % (name, like, author, mub,date))
    if nub == 1:
        print('主题,%s,%s,%s,id%s,时间%s' % (name, like, author, mub,date))
    if nub == 2:
        print('气泡,%s,%s,%s,id%s,时间%s' % (name, like, author, mub,date))
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

if __name__ == '__main__':
    headers('ptcz=524226d2afe911330fbfb452ece92c88adaf537005227086da273eb7e9063cd5; pgv_pvi=2405019648; RK=8qQlllsT7n; pgv_pvid=6010152923; ts_refer=ui.ptlogin2.qq.com/; ts_uid=5448687400; uin=o1542183954; skey=@ylqMCcxA0; p_uin=o1542183954; pt4_token=zIt0WsJnGfr7Wu9WOAR2dfkct2LMd0dVv43haveB5aw_; p_skey=nJEb3ppj-ZvxIftuW7MH2keeR7nEl32ZFBgGWK4-oV0_; pgv_info=ssid=s2982446144; ts_last=zb.vip.qq.com/v2/pages/beautyMall')

    obj = get_mysql.SqlHelper()
    aa = obj.get_list('SELECT * FROM `tenxun_business`',[])
    for a in aa:
        Updata_time('ylqMCcxA0',a['tenxun_business_id'])
    obj.close()
    # print(get_mysql.Time_Stamp(1592207153))
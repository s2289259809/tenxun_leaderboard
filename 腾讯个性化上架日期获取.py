import requests,json,time,datetime,re
from utils import sqlheper_my,log
import multiprocessing,random
logger = log.logger
import numpy as np
import threading
from concurrent.futures import ThreadPoolExecutor

def tenxun(zuozhe_id):
    global headers
    url = "https://zb.vip.qq.com/trpc/cgi?daid=18&g_tk=598248813"
    headers = {
      'authority': 'zb.vip.qq.com',
      'accept': 'application/json, text/plain, */*',
      'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; vivo Y67A Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045008 Mobile Safari/537.36 V1_AND_SQ_8.3.3_1376_YYB_D QQ/8.3.3.4515 NetType/WIFI WebP/0.3.0 Pixel/720 StatusBarHeight/49 SimpleUISwitch/0 QQTheme/1000',
      'content-type': 'application/json',
      'origin': 'https://zb.vip.qq.com',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-mode': 'cors',
      'sec-fetch-dest': 'empty',
      'referer': 'https://zb.vip.qq.com/v2/pages/beautyMall?supplyerid=1110606318',
      'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
      'cookie': 'RK=mAoxtFe2EH; ptcz=fa47b54d538524c1369918c43dac7126fd158182ff0de9efa00b4c1a3ff2b76d; ts_refer=ui.ptlogin2.qq.com/; ts_uid=4578248000; pgv_pvid=8001024667; uin=o0657110547; p_uin=o0657110547; pgv_info=ssid=s1229988218; skey=@j5riYN0I0; pt4_token=fmQHELo6fWe908qR9ImJMsQDVFCjIMtrlz1RuvlL57g_; p_skey=kOnaA5owzoi6FfeylNIaLySFz6v297krHsmR3hC*t*k_; ts_last=zb.vip.qq.com/v2/pages/beautyMall'
    }
    for i in range(0,7):
        print(i*20,i*20+20)
        payload="{\"namespace\":\"beautyMall\",\"cmd\":\"SupplyerInfo\",\"data\":{\"stlogin\":{\"ikeytype\":1,\"iopplat\":3,\"uin\":657110547,\"sclientip\":\"\",\"skey\":\"@lC7bwyie7\"},\"supplyerid\":"+str(zuozhe_id)+",\"nextID\":"+str(i*20)+",\"Pagesize\":20}}"
        print(payload)
        # print(response.text)
        err = 0
        while True:
            response = requests.request("POST", url, headers=headers, data=payload)
            print(response)
            try:
                print('第%s页'%(i+1))
                tenxun_json(response.text)
                time.sleep(3)
                break
            except Exception as e:
                print(e)
                if err == 6:
                    logger.info('长期错误:%s'%zuozhe_id)
                    return
                if err != 6:
                    print('失败')
                    err+=1
                    time.sleep(10)
                    continue


def tenxun_json(txt):
    print('成功接收json')
    # a = open('json.txt',encoding='utf-8')
    a = json.loads(str(txt))
    # print(a['data'])
    zuozhe_name = a['data']['supplyername']
    data_list = []#上传数据库中
    for i in a['data']['rpt_openitem']:
        # print(i)
        leixing = i['appid']
        chanpin_ID = i['itemid']
        tupian = i['url']
        onlinetime = Timestamp_conversion(i['onlinetime'])

        aa = (leixing,chanpin_ID,tupian,onlinetime,)
        try:
            name = i['name']
            ab = (name,zuozhe_name,)
            aa = aa + ab
        except:
            like = 'null'
            ab = (like,zuozhe_name,)
            aa = aa + ab

        try:
            like = i['likecnt']
            ab = (like,)
            aa = aa + ab
            print(aa)
            data_list.append(aa)
        except:
            like = 0
            ab = (like,)
            aa = aa + ab
            print(aa)
            data_list.append(aa)

    obj =  sqlheper_my.SqlHelper()
    obj.multiple_modify(
        "INSERT INTO new_tenxun(types,tenxun_id,url,`date`,`name`,zuozhe,likes) VALUES(%s,%s,%s,%s,%s,%s,%s)",
        data_list)
    obj.close()

def Timestamp_conversion(nub):
    timeStamp = int(nub)
    dateArray = datetime.datetime.fromtimestamp(timeStamp)
    otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    return otherStyleTime

def Get_Name(Types,IDS):
    headers = {
        'authority': 'zb.vip.qq.com',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; vivo Y67A Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045008 Mobile Safari/537.36 V1_AND_SQ_8.3.3_1376_YYB_D QQ/8.3.3.4515 NetType/WIFI WebP/0.3.0 Pixel/720 StatusBarHeight/49 SimpleUISwitch/0 QQTheme/1000',
        'content-type': 'application/json',
        'origin': 'https://zb.vip.qq.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://zb.vip.qq.com/v2/pages/beautyMall?supplyerid=1110606318',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cookie': 'RK=mAoxtFe2EH; ptcz=fa47b54d538524c1369918c43dac7126fd158182ff0de9efa00b4c1a3ff2b76d; ts_refer=ui.ptlogin2.qq.com/; ts_uid=4578248000; pgv_pvid=8001024667; uin=o0657110547; p_uin=o0657110547; pgv_info=ssid=s1229988218; skey=@j5riYN0I0; pt4_token=fmQHELo6fWe908qR9ImJMsQDVFCjIMtrlz1RuvlL57g_; p_skey=kOnaA5owzoi6FfeylNIaLySFz6v297krHsmR3hC*t*k_; ts_last=zb.vip.qq.com/v2/pages/beautyMall'
    }
    url = "https://zb.vip.qq.com/v2/pages/itemDetail?appid="+str(Types)+"&itemid="+str(IDS)+"&_nav_titleclr=000000&_nav_txtclr=000000"
    ree = requests.get(url=url,headers=headers)
    name_re = re.findall('"appId":([0-9]*),"itemId":([0-9]*),"name":"(.*)","feeType":[0-9]*,"image"', ree.text)[0]
    print(name_re)
    type = name_re[0]
    id = name_re[1]
    name_s = name_re[2]
    obj =  sqlheper_my.SqlHelper()
    obj.modify(
        "UPDATE new_tenxun SET name_new=%s WHERE types=%s and tenxun_id = %s",
        [name_s,type,id])
    obj.close()
    # time.sleep(1.1)

if __name__ == '__main__':
    # Get_Name(2,40334)
    pool = multiprocessing.Pool(processes=3)
    aaa = open('C:\\Users\\22892\\Desktop\\new_tenxun.csv', encoding='utf-8')
    for i in aaa:
        ab = re.findall('([0-9]*),([0-9]*)', i.strip())[0]
        # Get_Name(ab[0], ab[1])
        pool.apply_async(Get_Name, (ab[0], ab[1]))
        time.sleep(random.uniform(0.5,1.2))# 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    pool.close()
    pool.join()
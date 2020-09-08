#coding:utf-8
import requests,re,time
import get_mysql
from multiprocessing import Pool,Manager,Process
import multiprocessing as mp

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; vivo Y67A Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045008 Mobile Safari/537.36 V1_AND_SQ_8.3.3_1376_YYB_D QQ/8.3.3.4515 NetType/WIFI WebP/0.3.0 Pixel/720 StatusBarHeight/49 SimpleUISwitch/0 QQTheme/1000',
    # 'cookie':str(denglu)
    'cookie': 'pgv_pvi=8369590272; RK=ekoduLjnSR; ptcz=38f4959b2f16ac0de36b998d9c0bb3f9a3410f4ba32aae8d9564420c8d092416; ts_refer=ui.ptlogin2.qq.com/cgi-bin/login; pgv_pvid=3781160700; ts_uid=6019751887; ptui_loginuin=1542183954; o_cookie=2289259809; pac_uid=1_2289259809; pgv_si=s3767843840; uin=o0657110547; skey=@ttVnBsHIX; p_uin=o0657110547; pt4_token=MSxgaTvJFOoQoBKKcDpl0S7xnyPXi-O2SjYYXEoVuv0_; p_skey=roARhkvVXKh8jHKLbDQJrYPWiIQneuv8MssZPZ2inNE_; pgv_info=ssid=s5931943050; ts_last=zb.vip.qq.com/v2/pages/itemDetail',
    'referer': 'https://zb.vip.qq.com/v2/pages/itemDetail?appid=2&itemid=10871&_nav_titleclr=000000&_nav_txtclr=000000',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
}

'''链接数据库'''
def get_sql(id_tenxun,name,like,type,author):
    '''主题：1
       气泡：2'''
    obj=get_mysql.SqlHelper()
    obj.modify('INSERT INTO tenxun_preview(tenxun_id,tenxun_name,likes,type,author) VALUES (%s,%s,%s,%s,%s)',[id_tenxun,name,like,type,author])
    obj.close()

def get_sql_update(id_tenxun,like):
    '''主题：1
       气泡：2'''
    obj=get_mysql.SqlHelper()
    obj.modify('UPDATE tenxun_preview SET likes = %s WHERE tenxun_id = %s',[like,id_tenxun])
    obj.close()

'''遍历获取'''
def data_collection_bubble(mub_bubble):
    error_bubble = 50
    # mub_bubble = 14583
    while True:
        if mub_bubble == 0:
            break
        else:
            url = 'https://zb.vip.qq.com/v2/pages/itemDetail?appid=2&itemid='+str(mub_bubble)+'&_nav_titleclr=000000&_nav_txtclr=000000'
            r=requests.get(url=url,headers=headers)
            r.encoding='utf-8'
            print(mub_bubble)
            if '提供' in r.text :
                name = re.findall('<p class="name" data-v-4c6112a2>(.*)</p><span',r.text,re.S)[0]
                like = re.findall('likeCount":([0-9]*)',r.text,re.S)[0]
                author = re.findall('由(.*)提供',r.text,re.S)[0]
                print(name,like,author)
                try:
                    get_sql(mub_bubble, name, like,'2',author)
                    print('提交正常')
                except:
                    get_sql_update(like,mub_bubble)
                    print('更新正常')

            else:
                error_bubble +=1
                print('无数据')
            mub_bubble -= 1

def data_collection_theme(mub_theme):
    error_theme = 50
    # mub_bubble = 14583
    while True:
        if mub_theme == 1000000:
            break
        else:
            url = 'https://zb.vip.qq.com/v2/pages/itemDetail?appid=3&itemid='+str(mub_theme)+'&_nav_titleclr=000000&_nav_txtclr=000000'
            r=requests.get(url=url,headers=headers)
            r.encoding='utf-8'
            print(mub_theme)
            if '提供' in r.text :
                name = re.findall('<p class="name" data-v-4c6112a2>(.*)</p><span',r.text,re.S)[0]
                like = re.findall('likeCount":([0-9]*)',r.text,re.S)[0]
                author = re.findall('由(.*)提供',r.text,re.S)[0]
                print(name,like,author)
                try:
                    get_sql(mub_theme, name, like,'1',author)
                    print('提交正常')
                except:
                    get_sql_update(like,mub_theme)
                    print('更新正常')

            else:
                error_theme +=1
                print('无数据')
            mub_theme -= 1
if __name__ == '__main__':
    # data_collection_bubble(14770)
    p = Process(target=data_collection_theme,args=(1019123,))
    pp = Process(target=data_collection_bubble,args=(16770,))
    p.start()
    pp.start()
    pp.join()
    p.join()


import requests
import json,time
import datetime
import pandas as pd

def ss():
    a = datetime.datetime.strptime('20200317', '%Y%m%d')
    print(a + datetime.timedelta(days=1))

def aa():
    url = 'https://qqui.qq.com/api/common/admin/DataModel?gtk='
    headers = {
        'cookie': 'CNZZDATA1277655852=126080414-1590031204-https%253A%252F%252Fqqui.qq.com%252F%7C1590031204; pgv_pvi=8369590272; RK=ekoduLjnSR; ptcz=38f4959b2f16ac0de36b998d9c0bb3f9a3410f4ba32aae8d9564420c8d092416; pgv_pvid=3781160700; ptui_loginuin=1542183954; pac_uid=1_2289259809; tvfe_boss_uuid=39e25883eefd9139; o_cookie=657110547; _qpsvr_localtk=1599471822400; quid=f29daa2beff0914cd62ee015dd8944fb; qticket=d875ecb791044a61aa288e84174e49f0; quin=2289259809',
        'origin': 'https://qqui.qq.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    start = datetime.datetime.strptime('20200906', '%Y%m%d')
    total = []
    for i in range(0,1):
        print(i)
        atime = start + datetime.timedelta(days=i)
        con = True
        page = 0
        while con:
            data = {"search_type": 2, "gte": atime.strftime('%Y%m%d'), "lte": atime.strftime('%Y%m%d'),
                    "appid": "1110311890", "from": page,
                    "item_type_name": "", "size": 50, "sort": 2}
            res = requests.post(url, headers=headers, data=data)
            page += 1
            # print(res.text)
            var2 = json.loads(res.json()['data']['resBody'])['hits']['hits']
            if len(var2) == 0:
                break
            for i in var2:
                a = []
                a.append(i['_source']['ftime'])
                a.append(i['_source']['item_id'])
                a.append(i['_source']['item_type_name'])
                a.append(i['_source']['item_name'])
                a.append(i['_source']['pay_money_yuan'])
                a.append(i['_source']['pay_user_num'])
                print(i['_source']['item_name'])
                total.append(a)
            time.sleep(0.3)

    df = pd.DataFrame(total, columns=["时间",'产品ID' ,'类型', '名字', '支付金额', '支付人数'])
    df.to_excel("E:/weiji.xlsx", index=False)


if __name__ == '__main__':
    aa()
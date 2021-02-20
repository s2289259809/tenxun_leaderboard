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
        'cookie': 'pgv_pvi=8369590272; RK=ekoduLjnSR; ptcz=38f4959b2f16ac0de36b998d9c0bb3f9a3410f4ba32aae8d9564420c8d092416; pgv_pvid=3781160700; tvfe_boss_uuid=39e25883eefd9139; o_cookie=657110547; _ga=GA1.2.20279293.1603765697; pt_235db4a7=uid=iMKbC5DovVdcTsJlaVEo2Q&nid=0&vid=oBBwJA1a1tIdWVPkq0NgMg&vn=2&pvn=1&sact=1607476417354&to_flag=0&pl=0KzaISwJA-wYoyVB1nkjpQ*pt*1607476417354; iip=0; pac_uid=1_657110547; ptui_loginuin=1542183954; luin=o1542183954; lskey=0001000033396806ca71f147b3bc04dc6cd5d83685fe63ba6c777ed2e6484357e7cd32569996c750e764ab4c; vfwebqq=eacf419d448ab820e10d03fee9dcea0da8226905fc8c499594caf12c63cc38cbf0ba722777573128; eas_sid=a1L6z1v2j5D7M4a3c4N043l5s5; pgv_info=ssid=s9458518136; LW_sid=I1J6z1J2r5y7R4A485g8B7B6K5; LW_uid=r1q6o1A2w5R7r404n598R7U6n7; lolqqcomrouteLine=index-tool_main_a20210205lunarbeast_index-tool_main_a20210122lunarpresent_a20210205lunarbeast; tokenParams=%3Fe_code%3D500134; _qpsvr_localtk=0.6101915078372668; uin=o2289259809; skey=@kE5dnVunF; IED_LOG_INFO2=userUin%3D2289259809%26nickName%3D%2525E6%25259F%252590%26nickname%3D%25E6%259F%2590%26userLoginTime%3D1612574554%26logtype%3Dqq%26loginType%3Dqq%26uin%3D2289259809; quid=f29daa2beff0914cd62ee015dd8944fb; qticket=59fa810b933b45f7eca26b087d129568; quin=2289259809',
        'origin': 'https://qqui.qq.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    start = datetime.datetime.strptime('20210201', '%Y%m%d')
    total = []
    for i in range(0,6):
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
    # for i in range(1010600, 1010000, -1):
    #     print(i)
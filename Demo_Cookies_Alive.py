import requests,time

url = "https://zb.vip.qq.com/trpc/cgi?daid=18&g_tk=1283182688"

payload="{\"namespace\":\"beautyMall\",\"cmd\":\"SupplyerInfo\",\"data\":{\"stlogin\":{\"ikeytype\":1,\"iopplat\":2,\"uin\":1542183954,\"sclientip\":\"\",\"skey\":\"@tb7CWyXq8\"},\"supplyerid\":1110633869,\"nextID\":20,\"Pagesize\":20}}"
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
  'cookie': 'ptcz=524226d2afe911330fbfb452ece92c88adaf537005227086da273eb7e9063cd5; pgv_pvi=2405019648; RK=8qQlllsT7n; pgv_pvid=6010152923; ts_refer=ui.ptlogin2.qq.com/; ts_uid=5448687400; uin=o1542183954; skey=@tb7CWyXq8; p_uin=o1542183954; pt4_token=mjvMMwYXW65l0yW8p8g1NnsU-FrHBvi9Mc*9yPHaAas_; p_skey=9hT6DngDJuv7kEu7P1dgzF3hFe89mo*PsoTCqVZl3UE_; pgv_info=ssid=s2262208794; uid=1542183954; sig=9hT6DngDJuv7kEu7P1dgzF3hFe89mo*PsoTCqVZl3UE_; user-type=1; appid=18; ts_last=zb.vip.qq.com/v2/pages/beautyMall'
}

def run():
    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)

if __name__ == '__main__':
    while True:
        print('run')
        run()
        time.sleep(900)
import requests
import json

openkey = ''  # 必填，不知道openkey哪里来的，抓包的时候/log上会有openkey，复制过来就好了
cookie = ''  # Cookie
key = ''  # server酱key，不填不通知

headers = {
    'Cookie': cookie,
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 QQJSSDK/1.0.0 Hippy/1.0 qua/V1_IPH_KG_6.21.8_449_APP_A qmkege/6.21.8 GDTMobSDK/4.10.36',
    'Content-Type': 'application/json',
    'Referer': 'https://kg.qq.com/vMission/index.html?hippy=vMission',
    'Host': 'node.kg.qq.com',
    'No-Chunked': 'true'
}


def get_uid_from_cookie():
    kvs = cookie.split("; ")
    uid = ''
    for i in kvs:
        if i.find('uid=') >= 0:
            uid = i.split('=')[1]
    return uid


def _sign_in_():
    try:
        uid = get_uid_from_cookie()
        params = '{\"g_tk_openkey\":' + openkey + ',\"t_uid\":\"' + uid + '\",\"t_show_entry\":0,\"t_mapExtInfo\":{\"device_id\":\"\"},\"t_vctAppId\":[],\"ns\":\"KG_TASK\",\"cmd\":\"task.revisionSignInGetAward\",\"ns_inbuf\":\"\",\"mapExt\":{\"file\":\"taskJce\",\"cmdName\":\"GetSignInAwardReq\",\"l5api\":{\"modid\":503937,\"cmd\":589824},\"l5api_exp1\":{\"modid\":817089,\"cmd\":3801088}}}'
        sign_url = 'https://node.kg.qq.com/webapp/proxy?format=json&outCharset=utf-8&g_tk=' + openkey + '&g_tk_openkey=' + openkey
        msg = '';
        resp = requests.post(sign_url, data=params, headers=headers)
        # print(resp.text)
        awards_jo = json.loads(resp.text)['data']['task.revisionSignInGetAward']
        # awards_jo = json.loads(
        #     '{"total":1,"awards":[{"Id":22,"num":3,"desc":"","option":0,"confValue":"","mapExtInfo":{}},{"Id":22,"num":3,"desc":"","option":0,"confValue":"","mapExtInfo":{}}],"ret":0,"msg":"","lotteryStatus":0}')
        if awards_jo['total'] > 0:
            num = 0
            for award in awards_jo['awards']:
                num += award['num']
            msg = "获得鲜花" + str(num) + "个"
        else:
            msg = awards_jo['msg']
    except Exception:
        msg = 'cookie失效'
    return msg


def send_message(content):
    content = requests.get('https://sc.ftqq.com/' + key + '.send?text=全民K歌签到结果&desp=' + content).text


if __name__ == '__main__':
    msg = _sign_in_()
    print('msg: ', msg)
    if len(key) > 0:
        send_message(msg)

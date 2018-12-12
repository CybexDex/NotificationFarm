import logging, time, requests, json, os, datetime
# import hashlib

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='wechat.log',
                filemode='w')
logger = logging.getLogger('wechat')

class CybexWechatCorpHandler():
    def __init__(self, touser, agentid, corpid, secret):
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        self.__touser = touser
        self.__agentid = agentid
        self.__corpid = corpid
        self.__secret = secret

    def __get_token(self, corpid, secret):
        token_file = '/tmp/.{}.token.id'.format(corpid)
        try:
            with open(token_file, mode='r') as f:
                obj = json.loads(f.read())
                ts = datetime.strptime(obj['update_ts'], '%Y%m%d%H%M%S')
                time_delta = (datetime.now() - ts).total_seconds()
                if time_delta < 3600 and obj['secret'] == secret:
                    return obj['token']
        except Exception as e:
            pass

        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        data = {"corpid": corpid, "corpsecret": secret}
        r = requests.get(url = url, params = data, verify = False)
        logger.info(json.dumps(r.json()))
        token = r.json()['access_token']
        with open(token_file, mode='w') as f:
            f.write(json.dumps({
                      'token': token, 'secret': secret, 'update_ts': datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
                   }))
        return token

    def send(self,msg ):
        token = self.__get_token(self.__corpid, self.__secret)
        req_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(token)

        d = {
            'touser': self.__touser,
            'msgtype': 'text',
            'agentid': self.__agentid,
            'text': {
                'content':msg
            },
            'safe': '0'
        }
        # symbol = hashlib.md5((msg).encode('utf-8')).hexdigest()
        requests.post(url = req_url, data = json.dumps(d), verify = False)


class CybexWechatHandler():
    def __init__(self, appid, secret):
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        self.__appid = appid
        self.__secret = secret

    def __get_token(self, appid, secret):
        token_file = '/tmp/.{}.token.id'.format(appid)
        try:
            with open(token_file, mode='r') as f:
                obj = json.loads(f.read())
                ts = datetime.strptime(obj['update_ts'], '%Y%m%d%H%M%S')
                time_delta = (datetime.now() - ts).total_seconds()
                if time_delta < 3600 and obj['secret'] == secret:
                    return obj['token']
        except Exception as e:
            pass

        url = "https://api.weixin.qq.com/cgi-bin/token"
        data = {"appid": appid, "secret": secret, "grant_type":"client_credential"}
        r = requests.get(url = url, params = data, verify = False)
        logger.info(json.dumps(r.json()))
        token = r.json()['access_token']
        with open(token_file, mode='w') as f:
            f.write(json.dumps({
                      'token': token, 'secret': secret, 'update_ts': datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
                   }))
        return token

    def send(self,msg ):
        token = self.__get_token(self.__appid, self.__secret)
        # req_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(token)
        req_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send'
        param = {'access_token':token}
        d = {
            'msgtype': 'text',
            'appid': self.__appid,
            'text': {
                'content':msg
            },
            'safe': '0'
        }
        # symbol = hashlib.md5((msg).encode('utf-8')).hexdigest()
        r = requests.post(url = req_url, params = param , data = json.dumps(d), verify = False)
        logger.info(json.dumps(r.json()))

# https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx5114007c5499ae1b&secret=da83f0a8b5e339055bc3ea13406005b6
handler = CybexWechatHandler('wx5114007c5499ae1b', 'da83f0a8b5e339055bc3ea13406005b6')
handler.send('this is a test!')

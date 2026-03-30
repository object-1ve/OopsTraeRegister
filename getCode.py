import requests
from getmail import generate_email

SCRIPT_VERSION = "1.0.2"

headers = {
    "accept": "application/json, text/javascript",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.trae.ai",
    "priority": "u=1, i",
    "referer": "https://www.trae.ai/",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Google Chrome\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "x-tt-passport-csrf-token": "5efeeb0cbdf87969ddb46ea47f4018c0",
    "x-tt-passport-ttwid-ticket": "AaEKEH99zi5g3tK_QOXRBAoBYTzPffvENcuJQI7apzYk9CFV2gLofJI-mgYtJZeSKg=="
}
cookies = {
    "passport_csrf_token": "5efeeb0cbdf87969ddb46ea47f4018c0",
    "passport_csrf_token_default": "5efeeb0cbdf87969ddb46ea47f4018c0",
    "odin_tt": "7bba6f99fc0ed9f8fd89ca07919b765c65d9299ed99c8b09f400c7b09e323d04fafe24883ca92e7b432f582c9fc2c879fa9172948ec3b0d8969d5eaaa075de0a",
    "_twpid": "tw.1774872069714.231789119112842529",
    "_ga": "GA1.1.846106808.1774872070",
    "_gcl_au": "1.1.1536965374.1774872070",
    "_fbp": "fb.1.1774872070381.684173001674475408",
    "_clck": "1haac7z%5E2%5Eg4s%5E1%5E2280",
    "store-country-sign": "MEIEDOaGELsqfUEKSWCkvAQgL8FnGte2s1P1CcPC-E6PDOlBCcT215qx1xKPJerqrcgEECPyyaizLNS6-QX6SieaUJY",
    "sid_guard": "71002eef435a8c3d8d8940d398cd7385%7C1774872238%7C21600%7CMon%2C+30-Mar-2026+18%3A03%3A58+GMT",
    "uid_tt": "fcc4ff1878880656a70cd5d51b150f11",
    "uid_tt_ss": "fcc4ff1878880656a70cd5d51b150f11",
    "sid_tt": "71002eef435a8c3d8d8940d398cd7385",
    "sessionid": "71002eef435a8c3d8d8940d398cd7385",
    "sessionid_ss": "71002eef435a8c3d8d8940d398cd7385",
    "tt_session_tlb_tag": "sttt%7C4%7CcQAu70NajD2NiUDTmM1zhf________-zXcUgk5T-a0iUBp3RCkUqIcg0SEVCSUibXH2Zdmxcl6A%3D",
    "sid_ucp_v1": "1.0.1-KDk1YTNlODJkMGRkMmZhM2JmYzc1OTJkNTc5YjExOTVkMjk0ZGQ4ODgKChCuzanOBhjUqykQAxoCbXkiIDcxMDAyZWVmNDM1YThjM2Q4ZDg5NDBkMzk4Y2Q3Mzg1Mk4KIMcG--Hc_xNAnNh41_cPsLPDE5kB1GVBADJtst0Zu4U4EiAfCAYxFNdHW26hCBYj9NQLlaCRLAoRWx6xEVkraa_5KRgDIgZ0aWt0b2s",
    "ssid_ucp_v1": "1.0.1-KDk1YTNlODJkMGRkMmZhM2JmYzc1OTJkNTc5YjExOTVkMjk0ZGQ4ODgKChCuzanOBhjUqykQAxoCbXkiIDcxMDAyZWVmNDM1YThjM2Q4ZDg5NDBkMzk4Y2Q3Mzg1Mk4KIMcG--Hc_xNAnNh41_cPsLPDE5kB1GVBADJtst0Zu4U4EiAfCAYxFNdHW26hCBYj9NQLlaCRLAoRWx6xEVkraa_5KRgDIgZ0aWt0b2s",
    "ttwid": "1%7C0P9jAEoYfurOu_V7r80XHQrXTV1DSJuDen4aHFpLDIw%7C1774872239%7Caa16d6f2b6ca984a1e01ee8b2fe37b5b6c7d5d5e2fb4ac234e44e84b4b405201",
    "_uetsid": "2427e1e02c3011f1b34f1522ad77af04",
    "_uetvid": "24284a402c3011f19bb4d7517800c351",
    "_clsk": "36clis%5E1774872303082%5E7%5E1%5Ed.clarity.ms%2Fcollect",
    "_ga_GF2YEJBQ7P": "GS2.1.s1774872069$o1$g1$t1774872303$j59$l0$h0",
    "_ga_JVLR55T34K": "GS2.1.s1774872070$o1$g1$t1774872303$j59$l0$h1191912492",
    "msToken": "rCasLwylProYXfqC8BT8W9XdbOuJFtfhC4b-z0LNtejGHu0lB5dqkJGZ8AuhbeaWoJdrMzEvYyFWL9AMnM_ir_cnX2cfqG42yfBP2O9NjHuK1HrOVg3ahYp3Zw0cvzVke7H5YlM="
}
url = "https://ug-normal.trae.ai/passport/web/email/send_code/"
params = {
    "aid": "677332",
    "account_sdk_source": "web",
    "sdk_version": "2.1.10-tiktok",
    "language": "en",
    "verifyFp": "verify_mnd4zpeo_VfI7oBUi_fWUJ_4kHS_9XmO_8riTyA2Pe1Rg",
    "sign": "2cab44319d640f15b266323c07f841048f235fe9c8b6e2fa4344c7bbc0c3c126",
    "qs": "6466666a706b715a76616e5a766a7077666029646c612969646b62706462602976616e5a736077766c6a6b297360776c637c4375",
    "msToken": "1Xo1nY1d0pFQawUQpgn9tUKe1iofJ4etMctmQw-CyQ0GtXz_ObJ1PS6T26vMc6xDs5PcI5ZGZKAt-HMVebmchhCjbKc8BgfNOKbhWDzf3dT1x3bsSiOihYOrQe_DyWZqB8toXOA=",
    "X-Bogus": "DFSzswVLDL9xpMkTCqcN5K8obRXZ",
    "X-Gnarly": "M8Q9HhY-udvYYmImeIUJGl/YZhOue-n6eRzBIk-Y8Pbm548gnEf6A2dwMdMzpGqWrJFYAKpwkpmOizgf4rgyk0/Shg0/fz/PRZ15lZQTgKVZ4SJfTaOzZ4TXTHUYKaNa7ZJi8J3VuklIRMoZW78Y//d-fbASvu80Ruqyi-8k2b0F5li-VIOzHtxNIBl6oZQx0PTzC/s8gLaqkTrbpziIc4ws5oeZFkxu8rN3emuUUCyi/yx84EbDBl3NsU-AjChC58StqOcd-6BMH0yZ5gYEtrXAQsBrcmxCdeQg3W2Qa5v5"
}
email = generate_email(local_length=8, domain="sunix.eu.org")

data = {
    "type": "1",
    "email": email,
    "password": "",
    "email_logic_type": "2"
}
session = requests.Session()
session.trust_env = False

try:
    response = session.post(
        url,
        headers=headers,
        cookies=cookies,
        params=params,
        data=data,
        timeout=20,
        proxies={"http": None, "https": None}
    )
    print(email)
    print(response.text)
    print(response)
except requests.exceptions.RequestException as error:
    print(type(error).__name__)
    print(error)

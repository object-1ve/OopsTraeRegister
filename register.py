import requests


headers = {
    "accept": "application/json, text/javascript",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.trae.ai",
    "priority": "u=1, i",
    "referer": "https://www.trae.ai/sign-up",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Google Chrome\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "x-tt-passport-csrf-token": "5efeeb0cbdf87969ddb46ea47f4018c0"
}
cookies = {
    "i18next": "en",
    "s_v_web_id": "verify_mnd4zpeo_VfI7oBUi_fWUJ_4kHS_9XmO_8riTyA2Pe1Rg",
    "passport_csrf_token": "5efeeb0cbdf87969ddb46ea47f4018c0",
    "passport_csrf_token_default": "5efeeb0cbdf87969ddb46ea47f4018c0",
    "cc_cookie": "%7B%22categories%22%3A%5B%22essential%22%2C%22optional%22%5D%2C%22revision%22%3A0%2C%22data%22%3Anull%2C%22consentTimestamp%22%3A%222026-03-30T12%3A01%3A08.131Z%22%2C%22consentId%22%3A%22da5b723c-d5c8-41c5-8411-2b1d37f07f35%22%2C%22services%22%3A%7B%22essential%22%3A%5B%5D%2C%22optional%22%3A%5B%5D%7D%2C%22languageCode%22%3A%22en%22%2C%22lastConsentTimestamp%22%3A%222026-03-30T12%3A01%3A08.131Z%22%2C%22expirationTime%22%3A1790596868131%7D",
    "_twpid": "tw.1774872069714.231789119112842529",
    "_ga": "GA1.1.846106808.1774872070",
    "_fbp": "fb.1.1774872070381.684173001674475408",
    "_clck": "1haac7z%5E2%5Eg4s%5E1%5E2280",
    "odin_tt": "b63e66c784ed07f8e88f15fc1e644c5ef1070824f62c3dc2669d83cc09d46db937c6f0b86c3849f2826c796d842ff147a6d470f8dc49b7456bd7f8ed1012d569",
    "_gcl_au": "1.1.1536965374.1774872070.1546645718.1774874998.1774875061",
    "store-country-sign": "MEIEDImSZT5FkzUrjPCLxgQgi2UCr692oI863Xh7Hu9No4m5llb5vAndFm7hH04rDccEEJ2NMxFR1HmLjuf27wsKjRI",
    "sid_guard": "89811cd196c5f3d3abe0872809e64a76%7C1774875060%7C21600%7CMon%2C+30-Mar-2026+18%3A51%3A00+GMT",
    "uid_tt": "5d35b168379b38d6898beff375f55f63",
    "uid_tt_ss": "5d35b168379b38d6898beff375f55f63",
    "sid_tt": "89811cd196c5f3d3abe0872809e64a76",
    "sessionid": "89811cd196c5f3d3abe0872809e64a76",
    "sessionid_ss": "89811cd196c5f3d3abe0872809e64a76",
    "tt_session_tlb_tag": "sttt%7C3%7CiYEc0ZbF89Or4IcoCeZKdv_________RnbDYho4Sadp1czJWLNhwnKdQad047rI3Ne91Nyju2RU%3D",
    "sid_ucp_v1": "1.0.1-KDg4YmUzYzNiNGQyNjdlZGU1NDU0N2NiYWM4MmY4OGNmZjQ4ZjhlMzgKChC046nOBhjUqykQAxoCbXkiIDg5ODExY2QxOTZjNWYzZDNhYmUwODcyODA5ZTY0YTc2Mk4KIBXur458HIwCf0I4SgyyTnmBTrrA40tqtEdjpbG0qfIVEiDcCJYSeYF5b_JLoPyAKe0ECPk6HSHd-3O05GuI_sqaPxgDIgZ0aWt0b2s",
    "ssid_ucp_v1": "1.0.1-KDg4YmUzYzNiNGQyNjdlZGU1NDU0N2NiYWM4MmY4OGNmZjQ4ZjhlMzgKChC046nOBhjUqykQAxoCbXkiIDg5ODExY2QxOTZjNWYzZDNhYmUwODcyODA5ZTY0YTc2Mk4KIBXur458HIwCf0I4SgyyTnmBTrrA40tqtEdjpbG0qfIVEiDcCJYSeYF5b_JLoPyAKe0ECPk6HSHd-3O05GuI_sqaPxgDIgZ0aWt0b2s",
    "ttwid": "1%7C0P9jAEoYfurOu_V7r80XHQrXTV1DSJuDen4aHFpLDIw%7C1774875061%7C2cd7e5cc2ad3db5dd17bed06a35bab6f6c4ee82bcb56b7f7d91cc6cab43b04ef",
    "msToken": "YrFcd1hlbz7qHuD2oIQWl7W6FlgpHBpCQp8DnE7k7RxaoeJUs9zmL8Mat8AYTrT8WyDpSFpR5sV9SCkNJls1GxgzO3ylp5cBW7GsN7zTQK92o4vKCrrKNSzShTOsYsT-3lOqoA==",
    "_uetsid": "2427e1e02c3011f1b34f1522ad77af04",
    "_uetvid": "24284a402c3011f19bb4d7517800c351",
    "_clsk": "1w1h5gm%5E1774875126530%5E10%5E1%5Ed.clarity.ms%2Fcollect",
    "_ga_GF2YEJBQ7P": "GS2.1.s1774874986$o2$g1$t1774875126$j59$l0$h0",
    "_ga_JVLR55T34K": "GS2.1.s1774874986$o2$g1$t1774875126$j59$l0$h153438055"
}
url = "https://www.trae.ai/passport/web/email/register_verify_login/"
params = {
    "aid": "677332",
    "account_sdk_source": "web",
    "sdk_version": "2.1.10-tiktok",
    "language": "en",
    "verifyFp": "verify_mnd4zpeo_VfI7oBUi_fWUJ_4kHS_9XmO_8riTyA2Pe1Rg",
    "sign": "a72e282b5a3101e982cdcdcb30c77b48e5cf080a6e8725dd2daa48aec728574f",
    "qs": "6466666a706b715a76616e5a766a7077666029646c612969646b62706462602976616e5a736077766c6a6b297360776c637c4375",
    "msToken": "LLQqlrTT_P0BkoRwdXd61YfoIsKNuILEwl-Ztg5MqgoZaTLRSxLFnzVfDd0lDhkhLRroWY4d7MOnfMsYd0-J1Ufxx3ELTMj9H1nFh4PAc76zh1jzQZ-InC39Gm8Y2Sj-JCM8-A==",
    "X-Bogus": "DFSzswVL2CHa0MkTCqc9AY8obR1r",
    "X-Gnarly": "MCkgPwsyxnAsSi1zPptqihoxRdXrK5rOLuqRMxKJf4hJ-C-9osNKjJgEvuPeHyl7JfHH-4UCi5ltavFNsG-algebWvHBTwgwzXlMzNvm8ho2FS58oSPDgoecIsDgb3pCA-T4oURrMtITqPF4PNEUVE4VEB9b6smT4/RqXwW4sohNkWyBHRfvhowk-lcb0CzRBXGvFS/dtR6LZfbbV/4-0M/NnDFFcMtFepyAFNyiaKK6D2CRb/GJHFEshxm74tv3lUUycOQfb/KX7KVBCErajxZ0V/M3aSVMIHjJZAvFD7NX"
}
data = {
    "type": "1",
    "email": "mwxos9mn@sunix.eu.org",
    "password": "qwe123456",
    "code": "426378",
    "email_logic_type": "2"
}
response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)

print(response.text)
print(response)
import requests
from pathlib import Path
import os
import json

SCRIPT_VERSION = "1.0.2"

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://payauth.alipay.com",
    "priority": "u=1, i",
    "referer": "https://payauth.alipay.com/appAssign.htm?alipay_exterface_invoke_assign_target=invoke_5dc9288a908ab238443322c24f704880_uid85&alipay_exterface_invoke_assign_sign=_a_y_h_h_o_a_z048c_re47_t_quah_j_f_lt_gjxi_lo_uys_d_f_s_b_r2pm3h_owt_f_rd_p_vfu_q%3D%3D",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Google Chrome\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "JSESSIONID": "RZ42gFKVhPIA0yx1OOuhzW5Y7qnoNUsuperapiRZ42",
    "cna": "3VNRItQCFTACAXPfm1k54cUC",
    "jsh_t_c_e": "jsh_t_0.6130905507983002",
    "752459860": "QOohwmJJGsxge1vJLXglQXe%3DrAoSvAR2W7UAL7Lxv%2Bxd",
    "zone": "RZ42B",
    "ALIPAYJSESSIONID": "RZ42gFKVhPIA0yx1OOuhzW5Y7qnoNUsuperapiRZ42",
    "ctoken": "pZXsMlrKpkw8pkx7",
    "spanner": "9BDoMuxSpEdvY5bGcQAWcpyVzJJWQ7BJXt2T4qEYgj0="
}
url = "https://payauth.alipay.com/customer/querySignPageInfo.json"
params = {
    "ctoken": "pZXsMlrKpkw8pkx7"
}
data = {
    "_input_charset": "gbk",
    "i_c_i_d": "5dc9288a908ab238443322c24f704880_85",
    "json_ua": ""
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
    response.raise_for_status()
    payload = response.json()
    print(payload)
    login_success = payload.get("success") is True
    qr_code_info = payload.get("data", {}).get("qrCodeInfo", {})
    if not login_success:
        print("login not success")
        print(json.dumps(payload, ensure_ascii=False))
        raise ValueError("login failed, cannot fetch qrcode")
    img_url = qr_code_info.get("imgUrl")
    if not img_url:
        raise ValueError("imgUrl not found in response")
    img_response = session.get(
        img_url,
        headers={"user-agent": headers["user-agent"]},
        timeout=20,
        proxies={"http": None, "https": None}
    )
    img_response.raise_for_status()
    save_path = Path(__file__).with_name("alipay_qrcode.png")
    save_path.write_bytes(img_response.content)
    print(str(save_path))
    os.startfile(str(save_path))
except Exception as error:
    print(type(error).__name__)
    print(error)

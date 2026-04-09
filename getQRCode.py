import requests
from pathlib import Path
import os
import json
from urllib.parse import parse_qs, urlparse

SCRIPT_VERSION = "1.0.2"

json_path = Path(__file__).with_name("captured_send_code_params.json")
with open(json_path, "r", encoding="utf-8") as f:
    captured_params = json.load(f)

headers = captured_params.get("headers", {})
cookies = captured_params.get("cookies", {})
params = captured_params.get("params", {})

url = captured_params.get("url", "")
if url:
    if "?" in url:
        parsed = urlparse(url)
        url = parsed.scheme + "://" + parsed.netloc + parsed.path
        for key, values in parse_qs(parsed.query).items():
            if key not in params:
                params[key] = values[0] if len(values) == 1 else values
    else:
        parsed = urlparse(url)
        url = parsed.scheme + "://" + parsed.netloc + parsed.path

data = captured_params.get("post_data", {})
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
    print(params)
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

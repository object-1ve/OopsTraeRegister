import os
import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit
import requests


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("email", nargs="?", default=None)
    return parser.parse_args()


args = parse_args()
capture_path = Path(__file__).with_name("captured_send_code_params.json")
capture_data = json.loads(capture_path.read_text(encoding="utf-8"))
split_url = urlsplit(capture_data["url"])

url = f"{split_url.scheme}://{split_url.netloc}{split_url.path}"
params = capture_data["params"]
headers = capture_data["headers"]
data = capture_data["post_data"]
cookies = capture_data["cookies"]
custom_email = args.email or os.getenv("SEND_CODE_EMAIL")
if custom_email:
    data["email"] = custom_email
proxy_url = "http://127.0.0.1:7897"
proxies = {
    "http": proxy_url,
    "https": proxy_url
}
response = requests.post(url, headers=headers, params=params, data=data, cookies=cookies, proxies=proxies, timeout=20)

print(response.text)
print(response)

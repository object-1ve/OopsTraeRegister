import random
import re
import string
import sys
import requests

SCRIPT_VERSION = "1.0.4"
DEFAULT_DOMAIN = "sunix.eu.org"
DEFAULT_LENGTH = 8
ALPHABET = string.ascii_lowercase + string.digits
MAIL_LIST_URL = "https://mail.sunls.de/api/fetch"
HEADERS = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "priority": "u=1, i",
    "referer": "https://mail.sunls.de/",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Google Chrome\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}


def generate_email(local_length=DEFAULT_LENGTH, domain=DEFAULT_DOMAIN):
    local_part = "".join(random.choices(ALPHABET, k=local_length))
    return f"{local_part}@{domain}"


def request_json(url, timeout=20, params=None):
    session = requests.Session()
    session.trust_env = False
    request_kwargs = {
        "headers": HEADERS,
        "params": params,
        "timeout": timeout,
        "proxies": {"http": None, "https": None}
    }
    try:
        response = session.get(url, **request_kwargs)
    except requests.exceptions.SSLError:
        response = session.get(url, verify=False, **request_kwargs)
    response.raise_for_status()
    return response.json()


def fetch_mail_list(email, timeout=20):
    return request_json(MAIL_LIST_URL, timeout=timeout, params={"to": email})


def fetch_mail_detail(mail_id, timeout=20):
    return request_json(f"{MAIL_LIST_URL}/{mail_id}", timeout=timeout)


def extract_code(content):
    match = re.search(r">\s*(\d{6})\s*<", content)
    if match:
        return match.group(1)
    return None


def fetch_latest_mail_content(email, timeout=20):
    latest_list = fetch_mail_list(email=email, timeout=timeout)
    latest_meta = latest_list[0] if isinstance(latest_list, list) and latest_list else None
    latest_id = latest_meta.get("id") if isinstance(latest_meta, dict) else None
    if latest_id is None:
        return latest_meta, None, None
    detail = fetch_mail_detail(mail_id=latest_id, timeout=timeout)
    content = detail.get("content", "")
    code = extract_code(content)
    return latest_meta, detail, code


if __name__ == "__main__":
    target_email = sys.argv[1] if len(sys.argv) > 1 else generate_email()
    try:
        latest_meta, detail, code = fetch_latest_mail_content(target_email)
        print({"email": target_email, "latest": latest_meta, "code": code, "detail": detail})
    except requests.exceptions.RequestException as error:
        print(type(error).__name__)
        print(error)

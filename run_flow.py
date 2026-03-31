import argparse
import json
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime

from getmail import fetch_latest_mail_content
from getmail import generate_email
import requests

SCRIPT_VERSION = "1.0.9"
EMAIL_PATTERN = re.compile(r"[a-z0-9]{8}@sunix\.eu\.org")
SUCCESS_ACCOUNTS_FILE = "success_accounts.json"
SUCCESS_ACCOUNTS_LOCK = threading.Lock()
REGISTER_URL = "https://www.trae.ai/passport/web/email/register_verify_login/"
REGISTER_HEADERS = {
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
REGISTER_COOKIES = {
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
REGISTER_PARAMS = {
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


def send_code_and_get_email():
    print("[debug] start send code", flush=True)
    script_path = Path(__file__).with_name("getCode.py")
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    output = (result.stdout or "") + "\n" + (result.stderr or "")
    print(f"[debug] send code return code: {result.returncode}", flush=True)
    match = EMAIL_PATTERN.search(output)
    email = match.group(0) if match else None
    print(f"[debug] extracted email from output: {email}", flush=True)
    return email, result.returncode, output.strip()


def fetch_code_with_retry(email, retries=8, interval=2):
    latest_meta = None
    detail = None
    code = None
    last_error = None
    for index in range(retries):
        print(f"[debug] fetch try {index + 1}/{retries}, email={email}", flush=True)
        try:
            latest_meta, detail, code = fetch_latest_mail_content(email)
            last_error = None
            latest_id = latest_meta.get("id") if isinstance(latest_meta, dict) else None
            print(f"[debug] latest id: {latest_id}, code: {code}", flush=True)
        except requests.exceptions.RequestException as error:
            last_error = f"{type(error).__name__}: {error}"
            print(f"[debug] fetch error: {last_error}", flush=True)
            time.sleep(interval)
            continue
        if code:
            return latest_meta, detail, code, last_error
        time.sleep(interval)
    return latest_meta, detail, code, last_error


def register_account(email, code, password):
    print(f"[debug] start register, email={email}, code={code}", flush=True)
    session = requests.Session()
    session.trust_env = False
    response = session.post(
        REGISTER_URL,
        headers=REGISTER_HEADERS,
        cookies=REGISTER_COOKIES,
        params=REGISTER_PARAMS,
        data={
            "type": "1",
            "email": email,
            "password": password,
            "code": code,
            "email_logic_type": "2"
        },
        timeout=20,
        proxies={"http": None, "https": None}
    )
    print(f"[debug] register status: {response.status_code}", flush=True)
    return response


def save_success_account(email, password):
    save_path = Path(__file__).with_name(SUCCESS_ACCOUNTS_FILE)
    with SUCCESS_ACCOUNTS_LOCK:
        if save_path.exists():
            try:
                existing = json.loads(save_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                existing = []
        else:
            existing = []
        if not isinstance(existing, list):
            existing = []
        for item in existing:
            if isinstance(item, dict):
                created_at = item.get("created_at")
                if isinstance(created_at, int):
                    item["created_at"] = datetime.fromtimestamp(created_at).strftime("%Y-%m-%d_%H-%M-%S")
        existing.append(
            {
                "account": email,
                "password": password,
                "created_at": datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            }
        )
        save_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[debug] saved success account: {save_path}", flush=True)
    return str(save_path)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("forced_email", nargs="?", default=None)
    parser.add_argument("password", nargs="?", default="qwe123456")
    parser.add_argument("-n", "--count", type=int, default=1)
    parser.add_argument("-t", "--threads", type=int, default=3)
    return parser.parse_args()


def run_single_flow(forced_email, password, worker_index):
    if forced_email:
        email = forced_email
        code_return_code = None
        code_output = None
        print(f"[debug][worker-{worker_index}] use forced email: {email}", flush=True)
    else:
        email, code_return_code, code_output = send_code_and_get_email()
        if not email:
            email = generate_email()
            print(f"[debug][worker-{worker_index}] fallback generated email: {email}", flush=True)
    print(f"[debug][worker-{worker_index}] begin fetch code for email: {email}", flush=True)
    latest_meta, detail, code, fetch_error = fetch_code_with_retry(email=email)
    register_status = None
    register_text = None
    register_error = None
    register_success = False
    if code:
        try:
            register_response = register_account(email=email, code=code, password=password)
            register_status = register_response.status_code
            register_text = register_response.text
            if register_status == 200:
                register_payload = register_response.json()
                if register_payload.get("message") == "success":
                    save_success_account(email=email, password=password)
                    register_success = True
        except requests.exceptions.RequestException as error:
            register_error = f"{type(error).__name__}: {error}"
        except ValueError as error:
            register_error = f"{type(error).__name__}: {error}"
    return {
        "script_version": SCRIPT_VERSION,
        "worker_index": worker_index,
        "account": email,
        "password": password,
        "email": email,
        "code": code,
        "latest": latest_meta,
        "has_detail": detail is not None,
        "fetch_error": fetch_error,
        "register_status": register_status,
        "register_success": register_success,
        "register_text": register_text,
        "register_error": register_error,
        "send_code_return_code": code_return_code,
        "send_code_output": code_output
    }


def main():
    args = parse_args()
    count = max(1, args.count)
    threads = max(1, args.threads)
    if args.forced_email and count > 1:
        count = 1
    if count == 1:
        result = run_single_flow(
            forced_email=args.forced_email,
            password=args.password,
            worker_index=1
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    max_workers = min(threads, count)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                run_single_flow,
                forced_email=None,
                password=args.password,
                worker_index=index + 1
            )
            for index in range(count)
        ]
        results = [future.result() for future in as_completed(futures)]
    results.sort(key=lambda item: item["worker_index"])
    success_count = sum(1 for item in results if item.get("register_success"))
    print(
        json.dumps(
            {
                "script_version": SCRIPT_VERSION,
                "count": count,
                "threads": max_workers,
                "success_count": success_count,
                "results": results
            },
            ensure_ascii=False,
            indent=2
        )
    )


if __name__ == "__main__":
    main()

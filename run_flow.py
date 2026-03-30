import json
import re
import subprocess
import sys
import time
from pathlib import Path

from getmail import fetch_latest_mail_content
from getmail import generate_email
import requests

SCRIPT_VERSION = "1.0.4"
EMAIL_PATTERN = re.compile(r"[a-z0-9]{8}@sunix\.eu\.org")


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


def main():
    forced_email = sys.argv[1] if len(sys.argv) > 1 else None
    if forced_email:
        email = forced_email
        code_return_code = None
        code_output = None
        print(f"[debug] use forced email: {email}", flush=True)
    else:
        email, code_return_code, code_output = send_code_and_get_email()
        if not email:
            email = generate_email()
            print(f"[debug] fallback generated email: {email}", flush=True)
    print(f"[debug] begin fetch code for email: {email}", flush=True)
    latest_meta, detail, code, fetch_error = fetch_code_with_retry(email=email)
    print(
        json.dumps(
            {
                "script_version": SCRIPT_VERSION,
                "email": email,
                "code": code,
                "latest": latest_meta,
                "has_detail": detail is not None,
                "fetch_error": fetch_error,
                "send_code_return_code": code_return_code,
                "send_code_output": code_output
            },
            ensure_ascii=False,
            indent=2
        )
    )


if __name__ == "__main__":
    main()

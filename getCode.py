import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit
import requests
from getmail import generate_email

SCRIPT_VERSION = "1.0.3"
CAPTURE_FILE = "captured_send_code_params.json"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("email", nargs="?", default=None)
    return parser.parse_args()


def load_capture_payload():
    capture_path = Path(__file__).with_name(CAPTURE_FILE)
    capture_data = json.loads(capture_path.read_text(encoding="utf-8"))
    split_url = urlsplit(capture_data["url"])
    url = f"{split_url.scheme}://{split_url.netloc}{split_url.path}"
    return {
        "url": url,
        "params": dict(capture_data["params"]),
        "headers": dict(capture_data["headers"]),
        "cookies": dict(capture_data["cookies"]),
        "data": dict(capture_data["post_data"])
    }


def main():
    args = parse_args()
    payload = load_capture_payload()
    email = args.email or generate_email(local_length=8, domain="sunix.eu.org")
    payload["data"]["email"] = email
    session = requests.Session()
    session.trust_env = False
    try:
        response = session.post(
            payload["url"],
            headers=payload["headers"],
            cookies=payload["cookies"],
            params=payload["params"],
            data=payload["data"],
            timeout=20,
            proxies={"http": None, "https": None}
        )
        print(email)
        print(response.text)
        print(response)
    except requests.exceptions.RequestException as error:
        print(type(error).__name__)
        print(error)


if __name__ == "__main__":
    main()

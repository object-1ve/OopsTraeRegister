import json
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

from playwright.sync_api import sync_playwright


TARGET_PATH_FRAGMENT = "/passport/web/email/send_code"


def parse_query(url):
    return dict(parse_qsl(urlsplit(url).query, keep_blank_values=True))


def main():
    output_path = Path(__file__).with_name("captured_send_code_params.json")
    debug_path = Path(__file__).with_name("captured_send_code_debug.json")
    captured = {"matched": False}
    observed = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        def on_request(request):
            split = urlsplit(request.url)
            if TARGET_PATH_FRAGMENT not in split.path:
                return
            observed.append({"url": request.url, "method": request.method, "path": split.path})
            if captured["matched"]:
                return
            captured["matched"] = True
            captured["captured_at"] = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            captured["url"] = request.url
            captured["method"] = request.method
            captured["params"] = parse_query(request.url)
            captured["headers"] = request.headers
            try:
                captured["post_data"] = request.post_data_json
            except Exception:
                captured["post_data"] = request.post_data
            try:
                cookie_items = context.cookies("https://www.trae.ai")
                captured["cookies"] = {item["name"]: item["value"] for item in cookie_items}
            except Exception:
                captured["cookies"] = {}
            output_path.write_text(json.dumps(captured, ensure_ascii=False, indent=2), encoding="utf-8")
            print("captured:", output_path)
            print(json.dumps(captured, ensure_ascii=False, indent=2))

        page.on("request", on_request)
        page.goto("https://www.trae.ai/sign-up", wait_until="domcontentloaded")
        print("已打开注册页。请在页面触发一次发送验证码请求。")
        print("抓到请求后会自动写入 captured_send_code_params.json，然后关闭浏览器结束。")
        print("若 120 秒未抓到，会输出 captured_send_code_debug.json 供排查。")

        deadline = time.monotonic() + 120
        while not captured["matched"] and time.monotonic() < deadline:
            page.wait_for_timeout(500)
        if not captured["matched"]:
            debug_payload = {
                "matched": False,
                "checked_at": datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                "message": "未抓到 send_code 请求，请确认页面上确实点击了发送验证码。",
                "observed_count": len(observed),
                "observed": observed[:200]
            }
            debug_path.write_text(json.dumps(debug_payload, ensure_ascii=False, indent=2), encoding="utf-8")
            print("未截取到目标请求，已输出调试文件:", debug_path)

        browser.close()


if __name__ == "__main__":
    main()

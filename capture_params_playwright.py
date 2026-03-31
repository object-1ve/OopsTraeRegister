import json
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

from playwright.sync_api import sync_playwright


TARGET_PATH_FRAGMENT = "/passport/web/email/send_code"
EMAIL_INPUT_XPATH = "//*[@id=\"root\"]/div[1]/div[2]/div[4]/div[1]/div[1]/input"
SEND_CODE_XPATH = "//*[@id=\"root\"]/div[1]/div[2]/div[4]/div[2]/div[1]/div[2]"
AUTO_EMAIL = "123456@qq.com"
AUTO_RETRY_SECONDS = 20


def parse_query(url):
    return dict(parse_qsl(urlsplit(url).query, keep_blank_values=True))


def fill_email_and_click_send_code(page):
    deadline = time.monotonic() + AUTO_RETRY_SECONDS
    while time.monotonic() < deadline:
        try:
            page.wait_for_timeout(1000)
            page.wait_for_load_state("domcontentloaded", timeout=5000)
            email_input = page.locator(f"xpath={EMAIL_INPUT_XPATH}")
            send_button = page.locator(f"xpath={SEND_CODE_XPATH}")
            email_input.wait_for(state="visible", timeout=5000)
            email_input.fill(AUTO_EMAIL, timeout=5000)
            if email_input.input_value(timeout=3000) != AUTO_EMAIL:
                page.wait_for_timeout(400)
                continue
            email_input.press("Tab")
            page.wait_for_timeout(300)
            send_button.wait_for(state="visible", timeout=3000)
            send_button.click(timeout=3000)
            page.wait_for_timeout(500)
            return True
        except Exception:
            page.wait_for_timeout(500)
    return False


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
        clicked = fill_email_and_click_send_code(page)
        if clicked:
            print(f"已自动填入邮箱: {AUTO_EMAIL}")
            print("已自动点击 Send Code。")
        else:
            print("自动点击失败，将继续监听页面请求，建议手动点击 Send Code。")
        print("抓到请求后会自动写入 captured_send_code_params.json，然后关闭浏览器结束。")
        print("若 20 秒未抓到，会输出 captured_send_code_debug.json 供排查。")

        deadline = time.monotonic() + 20
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

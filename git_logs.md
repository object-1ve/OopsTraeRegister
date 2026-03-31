[1.0.16] 2026-03-31_21-47-10 改造 getCode.py：运行前从 captured_send_code_params.json 动态加载 url/params/headers/cookies/post_data，并在请求前覆盖 email 参数。
[1.0.17] 2026-03-31_21-55-01 改造 capture_params_playwright.py：自动填入 123456@qq.com 并点击 Send Code，触发后自动抓取 send_code 请求参数。
[1.0.18] 2026-03-31_21-59-05 优化 capture_params_playwright.py：新增自动填充与点击重试流程，避免页面刷新导致邮箱丢失后无法触发 Send Code。
[1.0.19] 2026-03-31_22-04-38 更新 README.md：补充参数抓取脚本说明、getCode.py 动态参数机制、依赖安装与推荐执行顺序。

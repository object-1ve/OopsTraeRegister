# OopsTraeRegister

OopsTraeRegister 是一个自动化注册 Trae 账号的工具脚本集合。当前流程支持“先自动抓取最新发码请求参数，再执行发码/收码/注册”，以降低参数过期带来的失败率。

## 功能特性

- **自动化注册流程**：串联邮箱生成、发码、收码、注册等步骤。
- **动态抓取发码参数**：通过 Playwright 监听页面请求并写入 `captured_send_code_params.json`。
- **发码前自动加载最新参数**：`getCode.py` 每次运行前都会读取抓包文件中的 `url/params/headers/cookies/post_data`。
- **临时邮箱与自动收码**：自动生成 `sunix.eu.org` 邮箱并提取 6 位验证码。
- **并发批量注册**：支持单次注册和多线程批量注册。
- **本地持久化**：注册成功信息自动写入 `success_accounts.json`。

## 核心文件结构

- `run_flow.py`：主流程控制脚本，串联获取邮箱、发码、收码和注册，支持并发执行。
- `capture_params_playwright.py`：打开注册页，自动填入邮箱并点击 Send Code，抓取发码请求参数。
- `captured_send_code_params.json`：保存最近一次抓取到的发码请求参数。
- `captured_send_code_debug.json`：抓包失败时输出的调试信息。
- `getCode.py`：发送注册验证码请求（运行前动态读取抓包参数）。
- `getmail.py`：轮询临时邮箱并提取验证码。
- `register.py`：注册逻辑核心参考。
- `getQRCode.py`：扫码相关逻辑，下载并展示二维码。
- `success_accounts.json`：注册成功后的账号数据保存文件。
- `git_logs.md`：项目版本及修改日志。

## 快速开始

### 依赖安装
确保已安装 Python 3，并安装依赖：

```bash
pip install requests playwright
playwright install chromium
```

### 1) 先抓取最新发码参数（推荐每次发码前执行）

```bash
python capture_params_playwright.py
```

脚本行为说明：
- 自动打开 `https://www.trae.ai/sign-up`
- 自动填入 `123456@qq.com` 并尝试点击 Send Code（含短时重试，降低页面刷新导致输入丢失的影响）
- 抓到 `/passport/web/email/send_code` 请求后写入 `captured_send_code_params.json`
- 若超时未抓到，会写入 `captured_send_code_debug.json` 便于排查

### 2) 发送验证码

不传邮箱时自动生成临时邮箱：

```bash
python getCode.py
```

传入指定邮箱：

```bash
python getCode.py your_email@example.com
```

### 3) 执行注册主流程

单个注册：

```bash
python run_flow.py
```

指定邮箱和密码：

```bash
python run_flow.py [指定邮箱] [指定密码]
```

批量并发注册：

```bash
python run_flow.py -n 10 -t 5
```

## 注意事项

- `captured_send_code_params.json` 中的参数可能随会话变化，建议定期重新抓取。
- 运行过程中可能受网络波动或目标服务器风控影响，脚本内置了异常捕获和重试降级机制。
- 注册成功账号会自动写入 `success_accounts.json`，并发场景已做写入冲突规避。
- 仅供学习和自动化测试参考，请合理使用。

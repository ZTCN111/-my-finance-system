from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)   # 打开有头浏览器
    page = browser.new_page()
    page.goto("https://xueqiu.com/statuses/v3/comments.json?id=340215740&size=20&max_id=-1")
    input("手动滑块验证完毕后按Enter继续")
    html = page.content()
    print(html)
    browser.close()
import requests
import time

# ========================
# 你的配置参数
# ========================

# 股票代码
code = "002104"

# 文章ID（你要爬的帖子ID）✅ 自己换成要爬的
artid = "1565303820"

# 每页多少条
pagesize = 30

# 接口地址
BASE_URL = "https://guba.eastmoney.com/api/getData"

# 这里换成你自己从浏览器复制的完整 Cookie
COOKIE = "st_inirUrl=https%3A%2F%2Fmguba.eastmoney.com%2Fmguba%2F; st_psi=20250628122338275-117001354293-7528993265; st_pvi=59394921597717; st_sn=3; st_sp=2025-06-28%2012%3A23%3A27; st_asi=delete; fullscreengg=1; fullscreengg2=1; qgqp_b_id=009fd27f95438f644f06c67d1affb630; st_si=48891344890375"

# Headers 尽量复制浏览器里的完整
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://guba.eastmoney.com",
    "Referer": f"http://guba.eastmoney.com/news,{code},{artid}.html",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15",
    "Cookie": COOKIE
}

# ========================
# 主逻辑
# ========================

all_comments = []
pageindex = 1

while True:
    print(f"\n[*] 正在抓取第 {pageindex} 页...")

    # POST 的表单参数
    data = {
        "code": code,
        "path": "reply/api/Reply/ArticleNewReplyList",
        "artid": artid,
        "pageindex": pageindex,
        "pagesize": pagesize
    }

    # 发POST请求
    try:
        resp = requests.post(BASE_URL, headers=headers, data=data, timeout=10)
    except Exception as e:
        print(f"[❌] 请求失败：{e}")
        break

    # 打印部分原始返回，方便调试
    print("[Raw Response Preview]", resp.text[:150], "...\n")

    # 尝试解析JSON
    try:
        data_json = resp.json()
    except Exception as e:
        print("[❌] 返回的不是JSON，可能被WAF拦截或被反爬，需要检查Cookie和Headers")
        break

    # 先判断 re 字段是否是 None
    re_data = data_json.get("re")
    if not re_data or not isinstance(re_data, dict):
        print("[✔️] 没有更多评论或接口re字段为null，抓取结束")
        break

    # 拿到评论列表
    reply_list = re_data.get("list", [])
    if not reply_list:
        print("[✔️] 这一页没有更多评论，抓取结束")
        break

    # 逐条打印并存
    for item in reply_list:
        comment = {
            "user": item.get("post_user", {}).get("nickname", "匿名用户"),
            "content": item.get("post_content", "").strip(),
            "time": item.get("post_publish_time", "")
        }
        all_comments.append(comment)
        print(f"  - {comment}")

    # 翻到下一页
    pageindex += 1
    time.sleep(1)

print("\n✅ 所有评论抓取完毕")
print(f"总共抓取了 {len(all_comments)} 条评论")
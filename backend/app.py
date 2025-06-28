from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import re
from transformers import pipeline

# ====================================
# 加载模型和初始化
# ====================================
sentiment_model = pipeline("sentiment-analysis", model="uer/roberta-base-finetuned-jd-binary-chinese")

app = Flask(__name__)
CORS(app)

# ====================================
# 数据库连接
# ====================================
client = MongoClient('mongodb://localhost:27017/')
db_post = client['post_info']

# ====================================
# 工具函数
# ====================================
def extract_code_from_url(url):
    match = re.search(r'news,([^,]+),', url)
    if match:
        code = match.group(1).strip()
        code = re.sub(r'^(zssh|zszx|bjsx)', '', code)
        return code
    return ""

# ====================================
# 路由
# ====================================
@app.route('/')
def home():
    return 'Hello, Financial Sentiment System with MongoDB!'


@app.route('/api/post/list')
def get_post_list():
    stock_code = request.args.get('code')
    if stock_code is None or stock_code.strip() == '':
        stock_code = '000001'
    else:
        stock_code = stock_code.strip().upper()
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 50))

    print(f"[INFO] Received request with stock_code={stock_code}")

    collections = db_post.list_collection_names()
    all_results = []

    for col_name in collections:
        if not col_name.startswith('post_'):
            continue

        collection = db_post[col_name]
        posts = collection.find()

        for post in posts:
            post_url = post.get('post_url', '')
            code_from_url = extract_code_from_url(post_url).upper()
            if not code_from_url:
                continue

            # 保留模糊搜索逻辑：只要输入股票代码在提取结果中出现就算匹配
            if stock_code and stock_code not in code_from_url:
                continue

            all_results.append({
                'id': str(post.get('_id')),
                'code': code_from_url,
                'title': post.get('post_title', ''),
                'view': post.get('post_view', ''),
                'comment_num': post.get('comment_num', 0),
                'url': post_url,
                'date': post.get('post_date', ''),
                'time': post.get('post_time', ''),
                'author': post.get('post_author', '')
            })

    # 按日期时间排序
    all_results.sort(key=lambda x: (x.get('date', ''), x.get('time', '')), reverse=True)

    total = len(all_results)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_results = all_results[start:end]

    # 只对当前页面的数据做批量情感分析
    batch_inputs = [f"{item.get('title', '')} {item.get('author', '')}".strip() or "空" for item in paginated_results]
    if batch_inputs:
        analyses = sentiment_model(batch_inputs)
        for item, analysis in zip(paginated_results, analyses):
            item['sentiment'] = analysis.get('label', '中性')
            item['score'] = float(analysis.get('score', 0.5))
    else:
        for item in paginated_results:
            item['sentiment'] = "中性"
            item['score'] = 0.5

    return jsonify({
        'total': total,
        'page': page,
        'page_size': page_size,
        'data': paginated_results
    })

if __name__ == '__main__':
    app.run(debug=True)
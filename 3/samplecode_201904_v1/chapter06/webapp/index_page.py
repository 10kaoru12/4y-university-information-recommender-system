
from bson.objectid import ObjectId
from datetime import datetime
from logging.handlers import RotatingFileHandler

from flask import Flask, request, render_template, make_response

import json
import logging
import pymongo   # pymongoを利用する
import uuid

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler('data/event.jsonl', maxBytes=100 * 10 ** 6, backupCount=3)
logger.addHandler(handler)


def _build_mongodb_client():
    # dockerネットワーク内ではmongoにより参照可能
    authority = "mongo:27017"

    client = pymongo.MongoClient(f"mongodb://{authority}")
    return client
    
    
def sure_objectid(str_or_bytes_or_objectid):
    return ObjectId(str_or_bytes_or_objectid)
    
    
def fetch_mongo_items(ids):
    client = _build_mongodb_client()    
    
    db = client["mynavi"]    
    collections = db["books"]
    
    ids = [ sure_objectid(id) for id in ids ] 
    items = list(collections.find({"_id": {"$in": ids}}))
    
    id2item = { item["_id"]: item for item in items}        
    return [id2item[id] for id in ids if id in id2item]    


def fetch_recommend_items():
    import requests
    api_authority = "api:8000"
    uri = f"http://{api_authority}/items"

    resp = requests.get(uri)
    app.logger.info(f"fetch {uri} {resp.status_code}")
    if resp.status_code != requests.codes.ok:
        app.logger.error("fetch_recommend_items: error")
        return []
        
    return resp.json().get("data", [])


@app.route('/')
def index():
    title = "Webアプリケーション"

    # ドキュメントIDをAPIから取得する
    _ids = fetch_recommend_items()
    _mongo_books = fetch_mongo_items(_ids)
    
    books = [
        {
            "id": str(book["_id"]),
            "title": book["title"],
            "image": book["image_url"],
            "category": book["genre"],
            "description": book["body"][:200] + '...',
            "link": "/",
            "context": json.dumps({
                "book_id": str(book["_id"]),  # コンテンツのID
                "position": idx,              # コンテンツの何番目の位置に表示されたか？
                "neighbors": _ids,            # 一緒に出現したコンテンツのID
            }),
        } for idx, book in enumerate(_mongo_books)
    ]
    return render_template('index.html', **locals())


@app.route('/log', methods=['GET', 'POST'])
def user_log():
    payload = request.get_data()
    payload = json.loads(payload.decode('utf8')) if payload else {}

    # requestオブジェクトからCookieを取得する
    uid = request.cookies.get('uid', None)

    # flaskのレスポンスオブジェクトの構築
    resp = make_response() 
    if uid is None:
        # Cookieがない場合はCookieを設定する
        uid = str(uuid.uuid4())
        
        # Cookieの設定を行う
        max_age = 60 * 60 * 24 * 3  # 3日間 有効
        expires = int(datetime.now().timestamp()) + max_age
        resp.set_cookie(
            'uid', value=uid,
            max_age=max_age,
            expires=expires,
            path='/',
            domain=request.host,    # Cookieは同一のホストのみで有効
            secure=True,            # httpsのみでCookieを送る
            httponly=True,          # JavascriptからのCookieの情報へのアクセスを制限する
        )    
                
    # ログにはユーザ識別可能なIDを埋め込む    
    payload['user_id'] = uid
    
    # 新しくに情報を追加で付与する
    payload['host'] = request.host                                    # ログの受信が行われたホスト 
    payload['path'] = request.referrer                                # クライアントでログの送信が行われたページ
    payload['received_at'] = int(datetime.now().timestamp() * 1000)   # サーバでのリクエストの処理時間 (javascriptと揃えるためミリ秒へ)

    payload['user_agent'] = {
        'raw': request.user_agent.string,                 # 念のため、生データは残しておく
        'platform': request.user_agent.platform,          # OSなどのプラットフォーム/デバイス情報 e.g. macos
        'browser': request.user_agent.browser,            # ブラウザ情報 e.g. chrome, safari
        'version': request.user_agent.version,            # ブラウザのバージョン情報
        'language': request.user_agent.language,          #
    }
    
    logger.info(json.dumps(payload))
    app.logger.info(payload)
    return resp, 204

if __name__ == '__main__':
    app.run()
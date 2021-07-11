
# ユーザが判別可能なロギング機構を構築する
from logging.handlers import RotatingFileHandler
from flask import Flask, request, render_template, make_response
from datetime import datetime

import logging
import json
import uuid

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler('data/event.jsonl', maxBytes=10000, backupCount=3)
logger.addHandler(handler)

@app.route('/')
def index():
    title = "Webアプリケーション"
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
        max_age = 60 * 60 * 24 * 3 # 3日間 有効
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
    app.run(debug=True)
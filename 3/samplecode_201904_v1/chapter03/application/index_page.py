import json
import requests
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index_page():
    title = "トップページ"
    if request.method == "GET":
        return render_template("hoge.html", **locals())
    else:
        text = request.form.get("text", "")
        payload = {"text": text}
        response = requests.post("http://localhost:8000/author_predict", data=json.dumps(payload))
        author = response.json()["author"]
        return render_template("hoge.html", **locals())

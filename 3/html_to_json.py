import glob
import json
import re
import sys

from bs4 import BeautifulSoup
from tqdm import tqdm


def main():
    with open("./valid_card_ids.txt", "r") as fin:
        valid_card_ids = set([line.strip() for line in fin])

    # globモジュールにより、対象ファイルのパスリストを取得します
    htmls = glob.glob("aozorabunko-master/cards/*/files/*.html")
    # 情報抽出できなかった数を数えます
    skip_count = 0

    # HTMLファイルを一つずつ処理します
    # tqdmはプログレスバーを表示します
    for path_to_html in tqdm(htmls):
        matched = re.search(r"(\d+)(_\d+)?.html$", path_to_html)
        if matched is None or matched.group(1) not in valid_card_ids:
            skip_count += 1
            print(f"Skipped.", file=sys.stderr)
            continue

        with open(path_to_html, mode="rb") as html:
          soup = BeautifulSoup(html, "lxml")

        try:
            story = extract_information(soup)
        except:
            skip_count += 1
            # 標準エラー出力とすることで、標準出力と別にします
            print("Skipped.", file=sys.stderr)

        story["id"] = matched.group(1)
        # ループの終了時にJSON形式で1行プリントします
        print(json.dumps(story, ensure_ascii=False))

    # 最後に総スキップ数を表示します
    print(f"Skip {skip_count} stories.", file=sys.stderr)


def extract_information(soup):
    # タイトルを取得します
    title = soup.find("h1", class_="title").text
    # 著者名を取得します
    author = soup.find("h2", class_="author").text

    # 本文箇所のHTMLを抽出します
    main_text = soup.find("div", class_="main_text")
    # ルビタグを削除します
    for elem in main_text.find_all(["rt", "rp", "h4"]):
        elem.decompose()
    # まず段落を取得し、次に文頭の空白を削除します
    paragraphs = [line.strip() for line in main_text.text.strip().splitlines()]
    # 今回は段落ごとに、改行文字を挿入します
    body = "\n".join(paragraphs)

    # 辞書型で返します
    return {"title": title, "author": author, "body": body}


if __name__ == "__main__":
    main()

import glob
import re
from bs4 import BeautifulSoup


def main():
    cards = glob.glob("./aozorabunko-master/cards/*/card*.html")
    story_metas = []
    for path_to_card in cards:
        card_id = path_to_id(path_to_card)
        if card_id is None:
            continue
        soup = load_html(path_to_card)
        if not valid_character_kind(soup):
            continue
        print(card_id)


def load_html(path_to_html):
    with open(path_to_html, "rt") as html:
        soup = BeautifulSoup(html, "lxml")
        return soup


def path_to_id(path):
    match = re.search(r"card(\d+).html$", path)
    if match:
        return match.group(1)


def valid_character_kind(soup):
    # 作品データテーブルの取得
    table = soup.find("table", attrs={"summary": "作品データ"})
    # tr要素を順に見る
    for tr in table.findAll("tr"):
        # 不要な改行は削除
        t = tr.text.replace("\n", "")
        # 仮名遣いに関する項目が、新字新仮名かどうか判定する
        if (t.startswith("文字遣い種別") or t.startswith("仮名遣い種別")) and t[7:] == "新字新仮名":
            return True
    return False


if __name__ == "__main__":
    main()

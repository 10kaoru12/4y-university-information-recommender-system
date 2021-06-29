import glob
import re
from bs4 import BeautifulSoup


def main():
    cards = glob.glob("aozorabunko-master/cards/*/card*.html")
    story_metas = []
    for path_to_card in cards:
        card_id = path_to_id(path_to_card)
        if card_id is None:
            continue
        soup = load_html(path_to_card)
        if not valid_character_kind(soup):
            continue
        print(card_id)


def path_to_id(path):
    match = re.search(r"card(\d+).html$", path)
    if match:
        return match.group(1)


def load_html(path_to_html):
    with open(path_to_html, "rb") as html:
        soup = BeautifulSoup(html, "lxml")
        return soup


def valid_character_kind(soup):
    table = soup.find("table", attrs={"summary": "作品データ"})
    for tr in table.findAll("tr"):
        t = tr.text.replace("\n", "")
        if(t.startswith("文字遣い種別") or t.startswith("仮名遣い種別")) and t[7:] == "新字新仮名":
            return True
        return False


if __name__ == "__main__":
    main()

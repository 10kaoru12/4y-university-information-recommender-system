# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from mynavi_tutorial.items import MynaviTutorialItem

class MynaviNewBooksSpider(scrapy.Spider):
    name = 'mynavi_new_books'
    allowed_domains = ['book.mynavi.jp']

    start_urls = [
        f"https://book.mynavi.jp/ec/products/?contents_type={ctype}"
        for ctype in [7, 17, 68, 80, 94, 107, 111, 114, 115, 123, 126, 131, 132]
    ]

    def parse(self, response):
        # 書籍を取得
        contents_type=urllib.parse.parse_qs(urllib.parse.urlparse(response.url).query)["contents_type"][0]
        links = [li.css("a::attr(href)").extract_first() for li in response.css("ul.category_list > li")]
        for href in links:
            yield response.follow(href, self.parse_book, meta={"contents_type": contents_type})

        if response.css("div.pager > ul > li"):
            next_pages = [
                li.css("a::attr(href)").extract_first()
                for li in response.css("div.pager > ul > li")
                if li.css("a::text").extract_first() == "≫"
            ]
            for next_page in next_pages[:1]:
                yield response.follow(next_page, self.parse)


    def parse_book(self, response):
        image_url = response.css("#item_sidebox > div > img::attr(src)").extract_first()
        yield MynaviTutorialItem(
            title="".join(response.css("h1.title::text").extract()),
            image_url=image_url,
            body="\n".join(response.css("h3::text, div.intro > p::text").extract()),
            genre=response.meta["contents_type"]
        )

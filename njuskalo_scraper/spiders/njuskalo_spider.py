# -*- coding: utf-8 -*-
import scrapy
from ..items import NjuskaloAd


def create_next_page_link(current_link, next_page_num):
    base_url = current_link.split('?')[0]
    return "{}?page={}".format(base_url, next_page_num)


class NjuskaloSpider(scrapy.Spider):
    name = 'njuskalo_spider'
    allowed_domains = ['njuskalo.hr']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = 'https://www.njuskalo.hr'

    def parse(self, response):
        articles = response.xpath(
            "//ul[@class='EntityList-items' and count(.//div[@class='entity-pub-date']) > 0]/li/article")
        for article in articles:
            title = article.xpath(".//h3[@class='entity-title']/a/text()").extract_first().strip()
            link = self.base_url + article.xpath(".//h3[@class='entity-title']/a/@href").extract_first().strip()
            description = article.xpath(".//div[@class='entity-description-main']/text()").extract()
            description = ', '.join(filter(None, map(lambda s: s.strip(), description)))
            published = article.xpath(".//div[@class='entity-pub-date']/time/text()").extract_first().strip()
            price = article.xpath(".//strong[@class='price price--eur']/text()").extract_first().strip().replace('.', '').replace(',', '')
            yield NjuskaloAd(
                title=title,
                link=link,
                description=description,
                published=published,
                price=price,
            )

        next_page_num = response.css(".Pagination-item--next").xpath(".//button/@data-page").extract_first()
        if next_page_num:
            yield scrapy.Request(url=create_next_page_link(response.url, next_page_num))

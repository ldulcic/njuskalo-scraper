# -*- coding: utf-8 -*-
import scrapy
from ..items import NjuskaloApartmentAd


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
            price = article.xpath(".//strong[@class='price price--eur']/text()").extract_first().strip()
            yield NjuskaloApartmentAd(
                title=title,
                link=link,
                description=description,
                published=published,
                price=price,
            )

        next_page_link = response.css(".Pagination-item--next").xpath(".//a/@href").extract_first()
        if next_page_link:
            yield scrapy.Request(url=next_page_link)

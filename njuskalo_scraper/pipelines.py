# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from njuskalo_scraper.database import NjuskaloApartmentAdDB


class DropDuplicatesPipeline:
    def process_item(self, item, spider):
        query = NjuskaloApartmentAdDB.select().where(NjuskaloApartmentAdDB.link == item['link'])
        if query.exists():
            raise DropItem("Duplicate item.")
        return item


class PersistItemsPipeline:
    def process_item(self, item, spider):
        NjuskaloApartmentAdDB.create(
            title=item['title'],
            link=item['link'],
            description=item['description'],
            published=item['published'],
            price=item['price']
        )
        return item

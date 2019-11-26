#!/usr/bin/env python3 -u

import argparse
import schedule
import time
import multiprocessing as mp
from scrapy.crawler import CrawlerProcess, Crawler
from scrapy import signals
from scrapy.utils.project import get_project_settings
from njuskalo_scraper.spiders.njuskalo_spider import NjuskaloSpider
from njuskalo_scraper.database import init_database, NjuskaloAdDB
from njuskalo_scraper.util import MailSender, parse_urls_file

mail_sender = MailSender()


def _crawl(queue, urls):
    items_scraped = []

    def item_scraped(item, response, spider):
        items_scraped.append(item)

    process = CrawlerProcess(get_project_settings())
    crawler = Crawler(NjuskaloSpider, get_project_settings())
    crawler.signals.connect(item_scraped, signals.item_scraped)
    process.crawl(crawler, start_urls=urls)
    process.start()
    queue.put(items_scraped)


def crawl(urls=None, first_run=False):
    q = mp.Queue()
    p = mp.Process(target=_crawl, args=(q, urls))
    p.start()
    items_scraped = q.get()
    p.join()

    if not first_run and items_scraped:
        mail_sender.send_email(items_scraped)


def parse_urls():
    args = argparse.ArgumentParser()
    group = args.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--urls', help='Comma separated njuskalo urls to scrape.')
    group.add_argument('-f', '--file', help='Path to file with urls. Every line of file contains njuskalo url.')
    args = args.parse_args()

    if hasattr(args, 'urls'):
        return list(map(lambda url: url.strip(), args.urls.split(',')))
    else:
        return parse_urls_file(args.file)


def main():
    init_database()
    urls = parse_urls()
    crawl(urls, first_run=not NjuskaloAdDB.select().exists())
    schedule.every(30).minutes.do(crawl, urls=urls)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping crawler...")
            break


if __name__ == '__main__':
    main()


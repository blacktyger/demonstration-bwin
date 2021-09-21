from bwin.spiders.tennis_spider import TennisSpider
from scrapy.crawler import CrawlerProcess
import os

if __name__ == '__main__':
    if os.path.isfile('file.json'):
        os.remove('file.json')

    def run():
        print('STARTING BWIN.COM TENNIS CRAWLER')
        process = CrawlerProcess({'FEED_FORMAT': 'json', 'FEED_URI': 'file.json'})
        crawler = process.create_crawler(TennisSpider)
        process.crawl(crawler)
        process.start()

        try:
            # END REPORT
            stats_dict = crawler.stats.get_stats()
            print('\n---------------------------')
            print(f"EVENTS ON PAGE: {stats_dict['to_scrape']}")
            print(f"SCRAPPED ITEMS: {stats_dict['item_scraped_count']}")
            print(f"COMPLETED EVENTS: {stats_dict['completed']}")
            print(f"REJECTED EVENTS: {stats_dict['rejected']}")
            print(f"ELAPSED TIME: {stats_dict['elapsed_time_seconds']}")
            print(f"FINISH REASON: {stats_dict['finish_reason']}")
            print('---------------------------')
        except Exception as e:
            print(e)

    run()
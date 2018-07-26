# -*- coding: utf-8 -*-

BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

DUPEFILTER_CLASS = "exts.dupefilter.RFPDupeFilter"
SCHEDULER = "exts.scheduler.Scheduler"
SCHEDULER_PERSIST = True

# ua配置
USER_AGENT = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# 爬虫并发数
CONCURRENT_REQUESTS = 16

#DOWNLOAD_DELAY = 3


# cookies配置
#COOKIES_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

DOWNLOADER_MIDDLEWARES = {
    #'scraper.middlewares.ScraperDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
}


SPIDERS_MIDDLEWARES = {
    'scrapy.spidermiddlewares.offsite': None,
}

ITEM_PIPELINES = {
    #'exts.pipelines.ZipfilePipelineWithFTP': 300,  # 文章
    'exts.pipelines.WeiboPipelineWithFTP': 300,     # 微博
}

# HTTP缓存
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


REDIS_HOST = 'localhost'
REDIS_PORT = 6379

MYSQL_HOST = 'localhost'
MYSQL_PORT = '3306'
MYSQL_USER = ''
MYSQL_PASSWORD = ''
MYSQL_DATABASE = 'info_sct'
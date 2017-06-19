# -*- coding: utf-8 -*-

import logging
import os
from time import time
import cookiejar as cj

log = logging.getLogger(__name__)

PARENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

STOPWORDS_DIR = os.path.join(PARENT_DIRECTORY, 'resources/text')

# NLP stopwords are != regular stopwords for now...
NLP_STOPWORDS_VI = os.path.join(
    PARENT_DIRECTORY, 'resources/misc/stopwords-nlp-vi.txt')
# NLP stopwords are != regular stopwords for now...
NLP_STOPWORDS_EN = os.path.join(
    PARENT_DIRECTORY, 'resources/misc/stopwords-nlp-en.txt')

NLP_STOPWORDS_JA = os.path.join(
    PARENT_DIRECTORY, 'resources/misc/stopwords-nlp-ja.txt')

DATA_DIRECTORY = '.newspaper_scraper'

TOP_DIRECTORY = os.path.join(os.path.expanduser("~"), DATA_DIRECTORY)
if not os.path.exists(TOP_DIRECTORY):
    os.mkdir(TOP_DIRECTORY)

# Error log
LOGFILE = os.path.join(TOP_DIRECTORY, 'newspaper_errors_%s.log' % time())
MONITOR_LOGFILE = os.path.join(
    TOP_DIRECTORY, 'newspaper_monitors_%s.log' % time())

# Memo directory (same for all concur crawlers)
MEMO_FILE = 'memoized'
MEMO_DIR = os.path.join(TOP_DIRECTORY, MEMO_FILE)

if not os.path.exists(MEMO_DIR):
    os.mkdir(MEMO_DIR)

# category and feed cache
CF_CACHE_DIRECTORY = 'feed_category_cache'
ANCHOR_DIRECTORY = os.path.join(TOP_DIRECTORY, CF_CACHE_DIRECTORY)

if not os.path.exists(ANCHOR_DIRECTORY):
    os.mkdir(ANCHOR_DIRECTORY)

TRENDING_URL = 'http://www.google.com/trends/hottrends/atom/feed?pn=p1'
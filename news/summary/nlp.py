# -*- coding: utf-8 -*-

import math
from pyvi.pyvi import ViTokenizer
from newspaper import Article
from collections import Counter
import tinysegmenter
import newspaper

import settings

with open(settings.NLP_STOPWORDS_VI, 'r') as f:
    stopwords = set([w.strip().replace(' ', '_') for w in f.readlines()])

ideal = 20.0

def tokenizer_content(content):
    return ViTokenizer.tokenize(content)

def set_stopwords(lang):
    global stopwords
    if lang == 'en':
        with open(settings.NLP_STOPWORDS_EN, 'r') as f:
            stopwords = set([w.strip().replace(' ', '_') for w in f.readlines()])
    elif lang == 'vi':
        with open(settings.NLP_STOPWORDS_VI, 'r') as f:
            stopwords = set([w.strip().replace(' ', '_') for w in f.readlines()])
    elif lang == 'ja':
        with open(settings.NLP_STOPWORDS_JA, 'r') as f:
            stopwords = set([w.strip().replace(' ', '_') for w in f.readlines()])
    else:
        with open(settings.NLP_STOPWORDS_VI, 'r') as f:
            stopwords = set([w.strip().replace(' ', '_') for w in f.readlines()])

def japanese_tokenizer(content):
    segmenter = tinysegmenter.TinySegmenter()
    return segmenter.tokenize(content)

def summarize(title='', text='', max_sents=5):
    if not text or not title or max_sents <= 0:
        return []

    summaries = []
    sentences = split_sentences(text)

    if len(sentences)*0.4 > max_sents:
        max_sents = int(len(sentences)*0.4)
    keys = keywords(text)
    titleWords = split_words(title)

    # Score sentences, and use the top of max_sents sentences
    ranks = score(sentences, titleWords, keys).most_common(max_sents)
    for rank in ranks:
        summaries.append(rank[0])
    summaries.sort(key=lambda summary: summary[0])
    return [summary[1] for summary in summaries]

def score(sentences, titleWords, keywords):
    """Score sentences based on different features
    """
    senSize = len(sentences)
    ranks = Counter()
    for i, s in enumerate(sentences):
        sentence = split_words(s)
        titleFeature = title_score(titleWords, sentence)
        sentenceLength = length_score(len(sentence))
        sentencePosition = different_sentence_position(i + 1, senSize)
        summation_based_selectionFeature = summation_based_selection(sentence, keywords)
        density_based_selectionFeature = density_based_selection(sentence, keywords)
        frequency = (summation_based_selectionFeature + density_based_selectionFeature) / 2.0 * 10.0
        # Weighted average of scores from four categories
        totalScore = (titleFeature*0.5 + frequency*2.0 +
                      sentenceLength*0.5 + sentencePosition*1.0)/4.0
        ranks[(i, s)] = totalScore
    return ranks


def summation_based_selection(words, keywords):
    score = 0.0
    if (len(words) == 0):
        return 0
    for word in words:
        if word in keywords:
            score += keywords[word]
    return (1.0 / math.fabs(len(words)) * score) / 10.0

def density_based_selection(words, keywords):
    if (len(words) == 0):
        return 0
    summ = 0
    first = []
    second = []

    for i, word in enumerate(words):
        if word in keywords:
            score = keywords[word]
            if first == []:
                first = [i, score]
            else:
                second = first
                first = [i, score]
                dif = first[0] - second[0]
                summ += (first[1] * second[1]) / (dif ** 2)
    # Number of intersections
    k = len(set(keywords.keys()).intersection(set(words))) + 1
    return (1 / (k * (k + 1.0)) * summ)


def split_words(text):
    """Split a string into array of words
    """
    try:
        # text = re.sub(r'[^\w ]', '', text)  # strip special chars
        return [x.strip('0123456789%@$.,=+-!;/()*"&^:#|\n\t').lower() for x in text.split()]
    except TypeError:
        return None


def keywords(text):
    """Get the top 10 keywords and remove stop words
    """
    NUM_KEYWORDS = 10
    text = split_words(text)
    # split words before removing blacklist words
    if text:
        nb_words = len(text)
        text = [x for x in text if x.encode('utf-8') not in stopwords]
        freq = {}
        for word in text:
            if word in freq:
                freq[word] += 1
            else:
                freq[word] = 1

        min_size = min(NUM_KEYWORDS, len(freq))
        keywords = sorted(freq.items(),
                          key=lambda x: (x[1], x[0]),
                          reverse=True)
        keywords = keywords[:min_size]
        keywords = dict((x, y) for x, y in keywords)

        for k in keywords:
            articleScore = keywords[k] / max(nb_words, 1)
            keywords[k] = articleScore * 1.5 + 1
        return dict(keywords)
    else:
        return dict()

def split_sentences(text):
    """Split a large string into sentences
    """
    import nltk.data
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    sentences = tokenizer.tokenize(text)
    sentences = [x.replace('\n', '') for x in sentences if len(x) > 10]
    return sentences


def length_score(sentence_len):
    return 1 - math.fabs(ideal - sentence_len) / ideal


def title_score(title, sentence):
    if title:
        title = [x for x in title if x.encode('utf-8') not in stopwords]
        count = 0.0
        for word in sentence:
            if (word.encode('utf-8') not in stopwords and word in title):
                count += 1.0
        return count / max(len(title), 1)
    else:
        return 0


def different_sentence_position(i, size):
    """Different sentence positions indicate different
    probability of being an important sentence.
    """
    normalized = i * 1.0 / size
    if (normalized > 1.0):
        return 0
    elif (normalized > 0.9):
        return 0.15
    elif (normalized > 0.8):
        return 0.04
    elif (normalized > 0.7):
        return 0.04
    elif (normalized > 0.6):
        return 0.06
    elif (normalized > 0.5):
        return 0.04
    elif (normalized > 0.4):
        return 0.05
    elif (normalized > 0.3):
        return 0.08
    elif (normalized > 0.2):
        return 0.14
    elif (normalized > 0.1):
        return 0.23
    elif (normalized > 0):
        return 0.17
    else:
        return 0

if __name__ == "__main__":
    url = 'http://www.nikkei.com/article/DGXLASDC21H0E_R20C17A6EAF000/'
    # japanese_sentences = "私の名前は中野です"
    #
    # print japanese_tokenizer(japanese_sentences.decode('utf-8'))
    # set_stopwords('ja')
    # print stopwords

    # article = Article(url.decode('utf-8'))
    # article.download()
    # article.parse()
    #
    # title = article.title
    # print title
    # print '-------------------'
    # content = article.text
    # print content
    # title_segmentation = tokenizer_content(content=title)
    # # print title_segmentation
    # segmentation = tokenizer_content(content=content)
    #
    # nlp_keywords = keywords(segmentation)
    # print nlp_keywords
    #
    # summary_sents = summarize(title=title_segmentation, text=segmentation, max_sents=7)
    # summary = '\n'.join(summary_sents)
    # summary = summary.replace('_', ' ')
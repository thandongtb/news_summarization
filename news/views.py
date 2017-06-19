# -*- coding: utf-8 -*-

from summary import nlp
from newspaper import Article
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def index(request):
    template = loader.get_template('news/index.html')
    return HttpResponse(template.render(context=None, request=request))

def result(request):
    url = request.POST['url']

    article = Article(url.decode('utf-8'))
    article.download()
    article.parse()

    title = article.title

    print type(title)

    content = article.text

    title_segmentation = nlp.tokenizer_content(content=title)
    segmentation = nlp.tokenizer_content(content=content)

    keywords = nlp.keywords(segmentation)

    summary_sents = nlp.summarize(title=title_segmentation, text=segmentation, max_sents=7)
    summary = '\n'.join(summary_sents)
    summary = summary.replace('_', ' ')

    template = loader.get_template('news/result.html')
    top_image = article.top_image
    context = {
        'title_summarization': title,
        'content_summarization': summary,
        'top_image': top_image,
        'keywords' : keywords
    }
    return HttpResponse(template.render(context, request))

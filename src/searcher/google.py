import json
import urllib2

from commonutil import dateutil

def _getUrl(keyword):
    jsonUrl = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q={q}'
    return jsonUrl.replace('{q}', urllib2.quote(keyword.encode('utf-8')))

def _fetch(url):
    try:
        req = urllib2.Request(url)
        res = urllib2.urlopen(req)
        content = res.read()
        res.close()
        responseText = content
    except Exception:
        responseText = None
    return responseText

def _parseGoogle(responseText, item2page):
    if not responseText:
        return None
    data = json.loads(responseText)
    if not data or not data.get('responseData') or 'results' not in data['responseData']:
        return None
    pages = []
    for item in data['responseData']['results']:
        pageItem = item2page(item)
        if pageItem:
            pages.append(pageItem)
    return pages

def _googleItem2page(item):
    pageItem = {}
    pageItem['title'] = item.get('title')
    pageItem['url'] = item.get('unescapedUrl')
    pageItem['content'] = item.get('content')
    return pageItem

def _parseGnews(responseText):
    return _parseGoogle(responseText, _googleItem2page)

def search(keyword):
    url = _getUrl(keyword)
    responseText = _fetch(url)
    return _parseGnews(responseText)


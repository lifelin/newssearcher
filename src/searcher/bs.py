
from commonutil import htmlutil
from . import gnews, google

def search(keyword):
    pages = gnews.search(keyword)
    if not pages:
        pages = google.search(keyword)
    if pages:
        for child in pages:
            if 'title' in child:
                child['title'] = htmlutil.getTextContent(child.get('title'))
            if 'content' in child:
                child['content'] = htmlutil.getTextContent(child.get('content'))
    return pages


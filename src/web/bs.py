
from searcher import gnews, google

def search(keyword):
    pages = gnews.search(keyword)
    if not pages:
        pages = google.search(keyword)
    return pages



from searchengine import gnews, google, twitter

def search(keyword):
    pages = gnews.search(keyword)
    if not pages:
        pages = google.search(keyword)
    return pages

def search4Test(keyword, twitterAccount):
    pages = []
    pages3 = gnews.search(keyword)
    pages.extend(pages3)
    if twitterAccount:
        pages3 = twitter.search(keyword, twitterAccount)
        pages.extend(pages3)
    pages3 = google.search(keyword)
    pages.extend(pages3)
    return pages


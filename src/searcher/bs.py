
from searchengine import gnews, google, twitter

def search(keyword):
    pages = gnews.search(keyword)
    if not pages:
        pages = google.search(keyword)
    return pages

def search4Test(keyword, twitterAccount):
    if not twitterAccount:
        return []
    pages3 = twitter.search(keyword, twitterAccount)
    return pages3


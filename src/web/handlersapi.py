import datetime
import json
import logging

from google.appengine.api import taskqueue

import webapp2

from commonutil import networkutil, stringutil, dateutil

from . import bs

_URL_TIMEOUT = 30
_FETCH_TRYCOUNT = 3
_CALLBACK_TRYCOUNT = 3

def _calculateHash(items):
    lines = []
    for item in items:
        url = item.get('url')
        if url:
            lines.append(url)
    return stringutil.calculateHash(lines)

class SearchRequest(webapp2.RequestHandler):
    def post(self):
        rawdata = self.request.body
        taskqueue.add(queue_name='default', payload=rawdata, url='/search/batch/')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Request is accepted.')


class BatchSearchRequest(webapp2.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        items = data['items']
        oldHash= data['hash']
        callbackurl = data['callbackurl']
        resultItems = []
        nnow14 = dateutil.getDateAs14(datetime.datetime.utcnow())
        for item in items:
            pages = bs.search(item['title'])
            if pages:
                resultPage = pages[0]
            else:
                resultPage = {}
            resultPage['keyword'] = item['title']
            resultPage['rank'] = item['rank']
            resultPage['keywordadded'] = item['added']
            resultPage['added'] = nnow14
            resultItems.append(resultPage)

        contentHash = _calculateHash(resultItems)
        if oldHash == contentHash:
            logging.info('No change fetch for %s.' % (data['origin'], ))
            return

        responseData = {
                'origin': data['origin'],
                'items': resultItems,
                'hash': contentHash,
        }

        success = networkutil.postData(callbackurl, responseData,
                    trycount=_CALLBACK_TRYCOUNT, timeout=_URL_TIMEOUT)
        if success:
            message = 'Push %s back to %s.' % (data['origin'], callbackurl)
        else:
            message = 'Failed to push %s back to %s.' % (data['origin'], callbackurl)
        logging.info(message)
        self.response.out.write(message)


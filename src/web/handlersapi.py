import json
import logging

from google.appengine.api import taskqueue

import webapp2

from commonutil import networkutil

import searcher.bs

_URL_TIMEOUT = 30
_FETCH_TRYCOUNT = 3
_CALLBACK_TRYCOUNT = 3

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
        for item in items:
            requestobj = {
                'callbackurl': data['callbackurl'],
                'origin': data['origin'],
                'item': item,
            }
            rawdata = json.dumps(requestobj)
            taskqueue.add(queue_name='default', payload=rawdata, url='/search/single/')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Put search task into queue.')


class SingleSearchResponse(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        data = json.loads(self.request.body)
        item = data['item']

        pages = searcher.bs.search(item['title'])
        if pages:
            resultPage = pages[0]
        else:
            resultPage = {}
        resultPage['keyword'] = item['title']
        resultPage['rank'] = item['rank']

        callbackurl = data['callbackurl']
        responseData = {
                'origin': data['origin'],
                'items': [resultPage],
        }
        success = networkutil.postData(callbackurl, responseData,
                    trycount=_CALLBACK_TRYCOUNT, timeout=_URL_TIMEOUT)
        if success:
            message = 'Push %s back to %s.' % (data['origin'], callbackurl)
        else:
            message = 'Failed to push %s back to %s.' % (data['origin'], callbackurl)
        logging.info(message)
        self.response.out.write(message)


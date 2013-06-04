import webapp2
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'library'))

import searcher
import searcher.handlers
import searcher.handlersapi

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')


app = webapp2.WSGIApplication([
('/', MainPage),
('/admin/test/', searcher.handlers.SearchNews),
('/api/search/', searcher.handlersapi.SearchRequest),
('/search/batch/', searcher.handlersapi.BatchSearchRequest),
],
debug=os.environ['SERVER_SOFTWARE'].startswith('Dev'))


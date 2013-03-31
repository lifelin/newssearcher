import webapp2
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'library'))

import configmanager.handlers

import web.handlers
import web.handlersapi

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')


app = webapp2.WSGIApplication([
('/', MainPage),
('/configitem/', configmanager.handlers.MainPage),
('/admin/test/', web.handlers.SearchNews),
('/api/search/', web.handlersapi.SearchRequest),
('/search/batch/', web.handlersapi.BatchSearchRequest),
],
                              debug=True)


import webapp2
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'library'))

import configmanager.handlers

import web.handlers

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')


app = webapp2.WSGIApplication([
('/', MainPage),
('/configitem/', configmanager.handlers.MainPage),
('/admin/searcher/test/', web.handlers.SearchNews),
],
                              debug=True)


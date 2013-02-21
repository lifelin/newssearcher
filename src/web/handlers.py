import os

from google.appengine.ext.webapp import template
import webapp2

from searcher import gnews

class SearchNews(webapp2.RequestHandler):
    def _render(self, templateValues):
        self.response.headers['Content-Type'] = 'text/html'
        path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
        self.response.out.write(template.render(path, templateValues))

    def get(self):
        templateValues = {
        }
        self._render(templateValues)

    def post(self):
        keyword = self.request.get('keyword').strip()
        pages = gnews.search(keyword)
        templateValues = {
            'keyword': keyword,
            'pages': pages,
        }
        self._render(templateValues)


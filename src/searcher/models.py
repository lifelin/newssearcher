import datetime

from commonutil import dateutil
from configmanager import cmapi

def _getItem(items, url):
    found = None
    for item in items:
        if item['url'] == url:
            found = item
            break
    return found

def _getKeyname():
    return 'url.history'

def getUrlAdded(url, added):
    items = cmapi.getItemValue(_getKeyname(), [],
                    modelname='RunStatus')
    found = _getItem(items, url)
    if found:
        found['count'] += 1
    else:
        found = {}
        found['count'] = 1
        found['url'] = url
        found['added'] = added
        items.append(found)
    found['updated'] = dateutil.getDateAs14(datetime.datetime.utcnow())
    start14 = dateutil.getHoursAs14(24)
    items = [ item for item in items if item['updated'] > start14 ]
    cmapi.saveItem(_getKeyname(), items,
                modelname='RunStatus')
    return found['added']


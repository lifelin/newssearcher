
from configmanager import cmapi

def getTwitterAccount():
    return cmapi.getItemValue('twitter.account', {})


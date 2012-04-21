import urllib, urllib2, cookielib,urlparse
import os
from contextlib import closing
from flexget.plugin import register_plugin

from BeautifulSoup import BeautifulSoup

BASE_PATH = 'http://www.italiansubs.net/index.php'

class Itasa(object):

    """
    rss: http://www.italiansubs.net/index.php?option=com_rsssub...  #myitasa or itasa subtitle feed
    accept_all: yes  #accept all from myitasa                                               
    itasa:
      username: itasaUsername
      password: itasaPassword
      path: ~/subtitle/download/folder # absolute or starting from $HOME
    """

    def validator(self):
        '''validator'''
        from flexget import validator
        d = validator.factory('dict')
        d.accept('text',key='username')
        d.accept('text',key='password')
        d.accept('text',key='path')
        return d

    def on_process_start(self, feed):
        '''Itasa login, storing cookie'''
        self.config = feed.config['itasa']

        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        login_data = urllib.urlencode({'username' : self.config['username']
                               , 'passwd' : self.config['password']
                               , 'Submit' :'Login'
                               , 'silent' : True
                               , 'option' : 'com_user'
                               , 'task'   : 'login'
                               , 'remember':'yes'})
        
        self.opener.open(BASE_PATH, login_data)

    def on_feed_download(self,feed):
        '''download zip file'''
        for entry in feed.entries:
            if entry.get('urls'):
                urls = entry.get('urls')
            else:
                urls = [entry['url']]
            for url in urls:
                with closing(self.opener.open(url)) as page:
                    z = self._zip(page)
                    filename = z.headers.dict['content-disposition'].split('=')[1]
                    filename = os.path.join(self.config['path'],filename)
                    filename = os.path.expanduser(filename)
                    with open(filename,'wb') as f:
                        f.write(z.read())

    def _zip(self,page):
        '''extract zip subtitle link from page, open download zip link'''
        content = page.read()
        start = content.index('<center><a href="')
        end = content.index('" rel',start)
        url = content[start+17:end]
        return self.opener.open(url)

    def _post_comment(self,page):
        soup = BeautifulSoup(page.read())
        form = soup.find(id='jc_commentForm')
        arg2_dict = []
        for input in form.findAll('input'):
            if input.name == 'jc_comment':
                arg2_dict.append([input.name,'grazie!!'])
            else:
                arg2_dict.append([input.name,input.value])

        data = { arg2: str(arg2_dict)
            , func   : "jcxAddComment"
            , task   : "azrul_ajax"
            , no_html: 1
            , option : jomcomment}
        
        self.opener.open(page.geturl(),data)

register_plugin(Itasa, 'itasa')

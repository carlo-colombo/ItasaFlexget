import urllib, urllib2, cookielib,urlparse
import os, random, re
from contextlib import closing
from BeautifulSoup import BeautifulSoup
import json

BASE_PATH = 'http://www.italiansubs.net/index.php'

class Itasa(object):

    """
    rss: http://www.italiansubs.net/index.php?option=com_rsssub...  #myitasa or itasa subtitle feed
    accept_all: yes  #accept all from myitasa                                               
    itasa:
      username: itasaUsername
      password: itasaPassword
      path: ~/subtitle/download/folder # absolute or starting from $HOME
      messages:
        - Grazie
        - Grazie mille!!!
        - Mitici
    """

    def validator(self):
        '''validator'''
        from flexget import validator
        d = validator.factory('dict')
        d.accept('text', key='username')
        d.accept('text', key='password')
        d.accept('text', key='path')
        d.accept('list', key='messages').accept('text')
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
        
        with closing(self.opener.open(BASE_PATH, login_data)) as page:
            if page.read().find('Nome utente e password non sono corrette') != -1:
                raise Exception("Wrong user or password")

    def on_task_download(self,feed):
        on_feed_download(self,feed)
    
    def on_task_download(self,feed):
        '''download zip file'''
        for entry in feed.entries:
            if entry.get('urls'):
                urls = entry.get('urls')
            else:
                urls = [entry['url']]
            for url in urls:
                with closing(self.opener.open(url)) as page:
                    try:
                        content = page.read()
                        z = self._zip(content)
                        filename = z.headers.dict['content-disposition'].split('=')[1]
                        filename = os.path.join(self.config['path'],filename)
                        filename = os.path.expanduser(filename)
                        soup = BeautifulSoup(content)
                        with open(filename,'wb') as f:
                            f.write(z.read())
                            entry['output'] = filename
                        if 'messages' in self.config :
                            self._post_comment(soup,page.geturl())
                        self._fill_fields(entry,soup)    
                    except ValueError:
                        print("Missing subtitle link in page: %s" % page.geturl())

    def _fill_fields(self,entry,soup):
        title = soup.find(id='remositoryfileinfo').find('center').string
        m = re.search("(.*?)[\s-]+(\d+)x(\d+)", title, re.UNICODE)
        if m:
            show_data = m.groups()
            entry['title'] = title.strip()
            entry['series_name'] = show_data[0].strip()
            entry['series_season'] = show_data[1].strip()
            entry['series_episode'] = show_data[2].strip()

    def _zip(self,content):
        '''extract zip subtitle link from page, open download zip link'''
        start = content.index('<center><a href="')
        end = content.index('" rel',start)
        url = content[start+17:end]
        return self.opener.open(url)

    def _post_comment(self,soup,url):
        form = soup.find(id='jc_commentForm')
        arg2_dict = []
        for inputTag in form.findAll('input'):
            if not inputTag['name'] == 'jc_name':
                arg2_dict.append([inputTag['name'],inputTag['value'] if inputTag.has_key('value') else None])

        m = self.config['messages']
        arg2_dict.append(['jc_comment',m[random.randint(0,len(m)-1)]  ])
        arg2_dict.append(['jc_name',self.config['username']])

        data = { 'arg2': json.dumps(arg2_dict)
            , 'func'   : "jcxAddComment"
            , 'task'   : "azrul_ajax"
            , 'no_html': 1
            , 'option' : "jomcomment"}
        
        return self.opener.open(url,urllib.urlencode(data))

try:
    from flexget.plugin import register_plugin
    register_plugin(Itasa, 'itasa')
except:
    pass
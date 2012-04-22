import unittest
from ItasaFlexGet import Itasa
from random import randint
import os
from contextlib import closing

import pdb

class ItasaFlexgetTests(unittest.TestCase):
    
    test_items = [
        ('Stargate.sg-1.s09e01.sub.itasa.fantascienza.zip','http://www.italiansubs.net/index.php?option=com_remository&Itemid=6&func=fileinfo&id=1789'),
        ('Knight.Rider.2008.s01e08.sub.itasa.zip','http://www.italiansubs.net/index.php?option=com_remository&Itemid=6&func=fileinfo&id=8269'),
        ('Six.Feet.Under.s04e05.sub.itasa.zip','http://www.italiansubs.net/index.php?option=com_remository&Itemid=6&func=fileinfo&id=148')
    ]

    @classmethod
    def setUpClass(cls):
        cls.username = raw_input('Itasa username: ')
        cls.password = raw_input('Itasa password: ')

    def setUp(self):
        self.feed = FeedConfigMock(self.username,self.password)
        self.test_item = ItasaFlexgetTests.test_items[randint(0,len(ItasaFlexgetTests.test_items)-1)]
        self.feed.entries[0]['url'] = self.test_item[1]

    def test_connection(self):
        ifg = Itasa()
        ifg.on_process_start(self.feed)

    def test_download(self):
        ifg = Itasa()
        ifg.on_process_start(self.feed) #connection
        ifg.on_feed_download(self.feed)
        self.assertTrue(os.path.exists(self.test_item[0]))

    def test_download_and_post_comment(self):
        ifg = Itasa()
        self.feed.config['itasa']['messages']=['Thank you','Thx']
        ifg.on_process_start(self.feed) #connection
        ifg.on_feed_download(self.feed)

    def test_html_parsing(self):
        ifg = Itasa()
        self.feed.config['itasa']['messages']=['Thank you','Thx']
        ifg.on_process_start(self.feed)
        with closing(ifg.opener.open(self.test_item[1])) as page:
            ifg._post_comment(page)

    def tearDown(self):
        '''remove downloaded test item from current directory'''
        if os.path.exists(self.test_item[0]):
            os.remove(self.test_item[0])


class FeedConfigMock(object):
    def __init__(self,username,password):
        self.config = {
            'itasa':{
                'username': username,
                'password': password,
                'path'    : '.'
            }
        }
        self.entries=[{
            'get': lambda x: None
        }]
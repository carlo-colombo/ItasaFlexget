Itasa Flexget plugin
====================

- [Flexget](http://www.flexget.com) 
- [Itasa](http://italiansubs.net)

Install
-------
Drop `ItasaFlexGet.py` in `~/.flexget/plugins`

Flexget config.yml examples
---------------------------
```
feeds:
  myitasa:
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
```
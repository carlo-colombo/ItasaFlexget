Itasa Flexget plugin
====================

- [Flexget](http://www.flexget.com) 
- [Itasa](http://italiansubs.net)
- [ItasaFlexget forum post on Itasa](http://www.italiansubs.net/forum/hardware-software/itasa-flexget-plugin/)

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

Features
---------------------------
* Optional parameter messages: plugin will post a message on subtitle page, message will be choose amongst configured messages.
* Extracted fields:
  * title
  * output _downloaded zip path_
  * series_name _Itasa version_
  * series_season
  * series_episode

Test
----------------------------
`python2 -m unittest test`
Test will ask for itasa username and password

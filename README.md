# SuperMarioMakerBookmarkApi
Fully written in Python3

##Installation
###From Github
Run `pip3 install https://github.com/lepelog/smmbookmarkapi/archive/master.zip`.

###From source
Clone the Repository, change to this directory and execute `python3 setup.py install`.

###Local installation
If you don't have root-privileges and/or want to install the package just for yourself, use the `--user`-Flag at the end of the command.

###Uninstall
To uninstall this package with pip run `pip3 uninstall smmbookmarkapi`

##Features
- Get informations about a level
- Bookmark a level or remove the bookmark of a level

##Usage
###Getting Information about a level
```python
>>> from smmbookmarkapi import SMMBookmarkApi
>>> api = SMMBookmarkApi()
>>> lvl = api.getstats('237B-0000-021E-7E0E')
>>> lvl.creator
'Olli'
>>> lvl.stars
'23'
```

###Bookmarking a level
TODO
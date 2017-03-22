# SuperMarioMakerBookmarkApi
Fully written in Python3

## Installation
### From Github
Run `pip3 install https://github.com/lepelog/smmbookmarkapi/archive/master.zip`.

### From source
Clone the Repository, change to this directory and execute `python3 setup.py install`.

### Local installation
If you don't have root-privileges and/or want to install the package just for yourself, use the `--user`-Flag at the end of the command.

### Uninstall
To uninstall this package with pip run `pip3 uninstall smmbookmarkapi`

## Features
- Get informations about a level
- Bookmark a level or remove the bookmark of a level

## Usage
### Getting Information about a level
```python
>>> from smmbookmarkapi import SMMBookmarkApi
>>> api = SMMBookmarkApi()
>>> lvl = api.getstats('237B-0000-021E-7E0E')
>>> lvl.creator
'Olli'
>>> lvl.stars
'23'
>>> lvl.name
'Chain Chomps Crazy Chaos Castle'
```

### Bookmarking a level
#### Notes about needed tokens
To bookmark a level, a session-cookie and a csrf-token is needed, but this token can by retrieved with the cookie. As far as I know, these never expire (WARNING, not sure at all, will test this), so you can get the cookie using [this help](https://makersofmario.com/help), requesting the csrf-token vith this programm and store it with the session-cookie for further requests. Example:
```python
>>> session_cookie = 'insertcookiedatahere'
>>> csrf_token = SMMBookmarkApi.get_token_for_session(session_cookie)
>>> csrf_token
'theretrievedtoken'
```
If you store it, you can use it in combination with the session-cookie to bookmark level:
```python
>>> from smmbookmarkapi import SMMBookmarkApi
>>> api = SMMBookmarkApi(csrf_token='theretrievedtoken', smmbookmark_session='insertcookiedatahere')
```
#### Using the bookmark-function
```python
>>> api.bookmark('LEVEL-ID') #Bookmark a level by id
>>> lvl.bookmark()           #Bookmark this course-object
>>> api,remove_bookmark('LEVEL-ID')
>>> lvl.remove_bookmark()
```
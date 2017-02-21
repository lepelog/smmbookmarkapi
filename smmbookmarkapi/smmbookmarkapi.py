import requests
import xml.etree.ElementTree as ET
import inspect
import re

#Namespace for xml-parsing
_namespace = '{http://namespaces.blar.de/mariomaker}'

class CourseNotFound(Exception):
    """
    Exception, if the requested course wasn't found
    Attribute id is the failing levelid
    """
    def __init__(self, id):
        super().__init__('Course with id "%s" not found!'%id)
        self.id=id
        
class BookmarkError(Exception):
    """
    Exception, if an Error occured during Bookmarking/removing Bookmark
    Attribute id is the failing levelid
    Attribute response is the requests-response from the smmbookmark
    """
    def __init__(self, id, response):
        super().__init__('Error during Bookmark operation with "%s"!'%id)
        self.id=id
        self.response=response

class SMMBookmarkApi:
    """
    Class for interacting with the Super Mario Maker Bookmark Page
    To set/remove bookmarks, a session-cookie and a csrf-token are needed, but the csrf-token can be
    retrieved using the session-cookie and the static method `get_token_for_session`.
    https://makersofmario.com/help has a good explanation how to get the cookie and what is possible with that.
    
    """
    mmbasicaddress='https://supermariomakerbookmark.nintendo.net/'
    csrf_finder_regex=re.compile('<meta name="csrf-token" content="(?P<token>[a-zA-Z0-9/=+]+)" />')
    
    def __init__(self, csrf_token=None, smmbookmark_session=None):
        """
        Initialize a new MarioMakerApi
        Params:
            smmapikey (str): For detailed Information see documentation of this class
        """
        self.csrf_token=csrf_token
        self.smmbookmark_session=smmbookmark_session

    @staticmethod
    def get_token_for_session(smmbookmark_session):
        cookies = {'_supermariomakerbookmark_session':smmbookmark_session}
        response = requests.get(SMMBookmarkApi.mmbasicaddress,cookies=cookies)
        response.raise_for_status()
        match = SMMBookmarkApi.csrf_finder_regex.search(response.text)
        if match is None:
            return None
        token = match.group('token')
        if not token is None:
            return token
        else:
            return None

    def getstats(self,courseid):
        """
        Asks a webservice (http://www.blar.de/smm/) about the given course-ids stats.
        If recieving the data is unsuccessfull, returns None
        Params:
            courseid (str): The mm-CourseId, format: xxxx-xxxx-xxxx-xxxx
        Returns:
            (smmapi.Course) Course object containing useful information about the level
        Exception:
            CourseNotFound, if the couse couldnot be found
        """
        return Course(api=self, stats=_getstats(courseid))

    def _check_tokens(self):
        if self.smmbookmark_session is None:
            raise AttributeError('smmbookmark_session is None!')
        if self.csrf_token is None:
            raise AttributeError('csrf_token is None!')

    def bookmark(self, levelcode):
        """
        Bookmark the given level-id
        """
        self._check_tokens()
        headers = {'X-CSRF-Token':self.csrf_token}
        cookies = {'_supermariomakerbookmark_session':self.smmbookmark_session}
        response=requests.post(self.mmbasicaddress+'courses/'+levelcode+'/play_at_later', headers=headers, cookies=cookies)
        if response.status_code != 200:
            raise BookmarkError(levelcode,response)

    def remove_bookmark(self, levelcode):
        """
        Remove Bookmark of the given level-id
        """
        self._check_tokens()
        headers = {'X-CSRF-Token':self.csrf_token}
        cookies = {'_supermariomakerbookmark_session':self.smmbookmark_session}
        response=requests.delete(self.mmbasicaddress+'bookmarks/'+levelcode, headers=headers, cookies=cookies)
        if response.status_code != 200:
            raise BookmarkError(levelcode,response)

class Course:
    """
    Representation of a Mario Maker Course, containing attributes:
        title: leveltitle
        code: levelcode, same as param
        type: levelstyle; SMB, SMB3, SMW or NSMBU
        clears: times, the level was cleared
        tries: times, level was tried, including clears
        plays: numbers of user who played the level
        clearrate: clears/tries
        stars: number of stars
        created: date, the level was created
        firstclear: user, who completed the level the first time
        creator: user, who created the level
    """
    
    def __init__(self, api, stats):
        if api is None:
            raise AttributeError('No Api given!')
        self.api=api
        if not stats is None:
            self.stats=stats
        else:
            raise AttributeError('No stats given!')

    def __getattr__(self, attr):
        if attr in self.stats:
            return self.stats[attr]
        else:
            raise AttributeError('%s is not in %s'%(attr, dir(self)))

    def bookmark(self):
        """
        Bookmark this level
        If this level is already bookmarked, do nothing
        """
        self.api.bookmark(self.code)

    def remove_bookmark(self):
        """
        Remove the Bookmark of this level
        If there was no Bookmark of this level, do nothing
        """
        self.api.remove_bookmark(self.code)

    def __dir__(self):
        return list(self.stats.keys())+list(self.__dict__.keys())+[i[0] for i in inspect.getmembers(self.__class__)]

def _getstats(courseid):
    """
    Asks a webservice (http://www.blar.de/smm/) about the given course-ids stats.
    If recieving the data is unsuccessfull, returns None
    Params:
        courseid (str): The mm-CourseId, format: xxxx-xxxx-xxxx-xxxx
    Returns:
        dict with levelstats
        None, if an error occured
    """
    raw = requests.get('http://www.blar.de/smm/fetch?code=%s'%courseid)
    #Expecting 200
    if raw.status_code!=200:
        return None
    
    level = ET.fromstring(raw.text)
    #print(raw.text)#For Debugging 
    stats = {
        'title': level.find(_namespace+'title').text,
        'code': level.find(_namespace+'code').text,
        'type': level.find(_namespace+'type').text,
        'clears': level.find(_namespace+'statistics/'+_namespace+'solved').text,
        'tries': level.find(_namespace+'statistics/'+_namespace+'tried').text,
        'plays': level.find(_namespace+'statistics/'+_namespace+'played').text,
        'clearrate': _noneto0(level.find(_namespace+'statistics/'+_namespace+'clear-rate').text),
        'stars': level.find(_namespace+'statistics/'+_namespace+'rated').text,
        'created':  level.find(_namespace+'created').text,
        'creator': _parseuser(level,'creator'),
        'firstclear': _parseuser(level,'first'),
    }
    return stats

def _parseuser(level, elemname):
    """
    Parses an user from the given ETree level, used for creator and first clear
    """
    try:
        return level.find(_namespace+elemname+'/'+_namespace+'user/'+_namespace+'name').text
    except AttributeError:
        return None

def _noneto0(a):
    if a == None:
        return '0'
    else:
        return a

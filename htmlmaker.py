#coding=utf-8

import urllib
import urllib2
import xml.etree.ElementTree as etree 
import re
import sys, os

class Htmlmaker:
    
    def __init__(self, email, passwd):
        self.email = email
        self.passwd = passwd

    def login(self, email, passwd):
        LOGIN_URL = 'https://www.google.com/accounts/ClientLogin'
        request = urllib2.Request(LOGIN_URL, urllib.urlencode({
            'service': 'reader',
            'Email': email,
            'Passwd': passwd
        }))

        f = urllib2.urlopen(request)
        lines = f.read().split()
        auth = lines[2][5:]
        sid = lines[0][4:]
        return (auth, sid)

    def get_unread(self, auth, sid):
        headers = {'Authorization': 'GoogleLogin auth=' + auth, 'Cookie': sid}
        request = urllib2.Request("https://www.google.com/reader/atom/user/-/state/com.google/reading-list?xt=user/-/state/com.google/read", headers=headers)
        f = urllib2.urlopen(request)
        return f.read()

    def get_text(self, entry, name):
        all_things = entry.findall(name)
        for thing in all_things:
            return  thing.text.encode('utf-8')

    def get_entrys(self, xml):
        w3atom = '{http://www.w3.org/2005/Atom}'
        tree = etree.fromstring(xml)
        all_entrys = tree.findall(w3atom + 'entry')
        entrys = []
        for entry in all_entrys:
            tmp_entry = {}
            tmp_entry['title'] = self.get_text(entry, w3atom + 'title')
            tmp_entry['content'] = self.get_text(entry, w3atom + 'content')
            if (not tmp_entry['content']):
                tmp_entry['content'] = self.get_text(entry, w3atom + 'summary')
            entrys.append(tmp_entry)

        for entry in entrys:
            entry['content'] = re.sub('<img[^>]*>', '', entry['content']) 
            entry['content'] = re.sub('<iframe.*>.*<\/iframe>', '', entry['content'])
        return entrys

    def run(self):
        (auth, sid) = self.login(self.email, self.passwd)
        xml = self.get_unread(auth, sid)
        return self.get_entrys(xml)

if __name__ == '__main__':
    maker = Htmlmaker(sys.argv[1], sys.argv[2])
    print maker.run()

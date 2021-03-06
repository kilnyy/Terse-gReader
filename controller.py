#coding=utf-8

import urllib
import urllib2
import xml.etree.ElementTree as etree 
import re
import sys, os

class Controller:
    
    def __init__(self, email, passwd):
        self.auth, self.sid = self.login(email, passwd)

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
        return auth, sid

    def get_unread(self, auth, sid):
        headers = {'Authorization': 'GoogleLogin auth=' + auth, 'Cookie': sid}
        GET_UNREAD_URL = "https://www.google.com/reader/atom/user/-/state/com.google/reading-list?n=10&xt=user/-/state/com.google/read";
        request = urllib2.Request(GET_UNREAD_URL, headers=headers)
        f = urllib2.urlopen(request)
        return f.read()

    def get_single(self, node, name):
        all_things = node.findall(name)
        if len(all_things):
            return all_things[0]
        return None

    def get_text(self, node):
        if node is not None:
            return node.text.encode('utf-8')
        else:
            return ''

    def get_entrys(self, xml):
        w3atom = '{http://www.w3.org/2005/Atom}'
        tree = etree.fromstring(xml)
        all_entrys = tree.findall(w3atom + 'entry')
        entrys = []
        for entry in all_entrys:
            tmp_entry = {}
            tmp_entry['title'] = self.get_text(self.get_single(entry, w3atom + 'title'))
            tmp_entry['source'] = self.get_text(self.get_single(self.get_single(entry, w3atom + 'source'), w3atom + 'title'))
            tmp_entry['id'] = self.get_text(self.get_single(entry, w3atom + 'id'))
            tmp_entry['link'] = self.get_single(entry, w3atom + 'link').get('href','')
            tmp_entry['content'] = self.get_text(self.get_single(entry, w3atom + 'content'))
            if (not tmp_entry['content']):
                tmp_entry['content'] = self.get_text(self.get_single(entry, w3atom + 'summary'))
            entrys.append(tmp_entry)
        
        for entry in entrys:
            entry['content'] = re.sub('<img[^>]*>', '', entry['content']) 
            entry['content'] = re.sub('<iframe.*>.*<\/iframe>', '', entry['content'])
        return entrys

    def get_data(self):
        xml = self.get_unread(self.auth, self.sid)
        return self.get_entrys(xml)

    def get_token(self):
        TOKEN_URL = 'https://www.google.com/reader/api/0/token'
        headers = {'Authorization': 'GoogleLogin auth=' + self.auth, 'Cookie': self.sid}
        request = urllib2.Request(TOKEN_URL, headers=headers)
        f = urllib2.urlopen(request)
        return f.read()

    def do_read(self, entryid):
        token = self.get_token()
        EDIT_URL = 'https://www.google.com/reader/api/0/edit-tag'
        headers = {'Authorization': 'GoogleLogin auth=' + self.auth, 'Cookie': self.sid}
        request = urllib2.Request(
            EDIT_URL,
            urllib.urlencode({
                'i' : entryid,
                'async' : 'true',
                'T' : token,
                'a' : 'user/-/state/com.google/read'
                }),
            headers=headers
        )
        f = urllib2.urlopen(request)

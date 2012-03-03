#coding=utf-8

import urllib
import urllib2
import xml.etree.ElementTree as etree 
import re
import sys, os

def login(email, passwd):
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

def get_unread(auth, sid):
    headers = {'Authorization': 'GoogleLogin auth=' + auth, 'Cookie': sid}
    request = urllib2.Request("https://www.google.com/reader/atom/user/-/state/com.google/reading-list?xt=user/-/state/com.google/read", headers=headers)
    f = urllib2.urlopen(request)
    return f.read()

def get_html(xml):
    result = ""
    w3atom = '{http://www.w3.org/2005/Atom}'
    tree = etree.fromstring(xml)
    all_entrys = tree.findall(w3atom + 'entry')
    for entry in all_entrys:
        result += '<div class="entry rb">\n'
        all_titles = entry.findall(w3atom + 'title')
        for title in all_titles:
            result += "<h3>\n" + title.text.encode('utf-8') + "</h3>\n"
        all_content = entry.findall(w3atom + 'content')
        for content in all_content:
            result += '<div class="content">\n' + content.text.encode('utf-8') + "</div>\n"
        all_summary = entry.findall(w3atom + 'summary')
        for summary in all_summary:
            result += '<div class="content">\n' + summary.text.encode('utf-8') + "</div>\n"
        result += '</div>\n'
    result = re.sub('<img[^>]*>', '', result) 
    result = re.sub('<iframe.*>.*<\/iframe>', '', result)
    return result

if __name__ == '__main__':
    (auth, sid) = login(sys.argv[1], sys.argv[2])
    xml = get_unread(auth, sid)
    print get_html(xml)

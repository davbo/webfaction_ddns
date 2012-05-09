#!/usr/bin/python
import json
import urllib2
import xmlrpclib
import os

currentip = json.load(urllib2.urlopen('http://httpbin.org/ip'))['origin']

if not os.path.isfile('lastip'):
    f = open('lastip', 'w')
    f.close()
with open('lastip', 'r') as f:
    lastip = f.read()

if lastip != currentip:
    server = xmlrpclib.ServerProxy('https://api.webfaction.com/')
    session_id, account = server.login('username', 'password')
    server.delete_dns_override(session_id, 'your.domain.com')
    server.create_dns_override(session_id, 'your.domain.com', currentip, '', '', '', '')

    with open('lastip', 'w') as f:
        f.write(currentip)

    print('IP updated to %s' % currentip)
else:
    print('IP not updated')

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import httplib
import urllib

headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}

NotAvailable = 9527

def ping(**kwargs):
    try:
        parameters = urllib.urlencode(kwargs)
        connection = httplib.HTTPConnection("test.local")
        connection.request("POST", "/ping.php", parameters, headers)
        response = connection.getresponse()
        data = response.read()
        connection.close()
        return response.status, response.reason, data
    except:
        return NotAvailable, "IGNORED", None

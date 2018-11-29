#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse

import eml_parser
import json
import datetime

def test():
    print("test")
    f = open("sample.txt")
    fullcontent = f.read()

    unitcontents = fullcontent.split("\n\n")
    #print(unitcontent[1])

    #print(unitcontent)

    for unitcontent in unitcontents:
        print(unitcontent.split("\n")[1:])

def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

def hyperlinktest():
    print("testmethod")
    with open('[NGP LDAP] Permission Summary.eml', 'rb') as fhdl:
        raw_email = fhdl.read()

    parsed_eml = eml_parser.eml_parser.decode_email_b(raw_email)
    print(json.dumps(parsed_eml, default=json_serial))
    # user_name_split()

if __name__ == '__main__':
    test()
    hyperlinktest()

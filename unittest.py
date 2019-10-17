#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import webbrowser
#https://docs.python.org/2/library/webbrowser.html
import email
from email import policy
from email.parser import BytesParser
import base64


def extract (msgfile, key):
    """Extracts all data from e-mail, including From, To, etc., and returns it as a dictionary.
    msgfile -- A file-like readable object
    key     -- Some ID string for that particular Message. Can be a file name or anything.
    Returns dict()
    Keys: from, to, subject, date, text, html, parts[, files]
    Key files will be present only when message contained binary files.
    For more see __doc__ for pullout() and caption() functions.
    """
    m = email.message_from_file(msgfile)
    From, To, Subject, Date = caption(m)
    #Text, Html, Files, Parts = pullout(m, key)
    Text = Text.strip(); Html = Html.strip()
    msg = {"subject": Subject, "from": From, "to": To, "date": Date,
        "text": Text, "html": Html, "parts": Parts}
    if Files: msg["files"] = Files
    return msg

def caption (origin):
    """Extracts: To, From, Subject and Date from email.Message() or mailbox.Message()
    origin -- Message() object
    Returns tuple(From, To, Subject, Date)
    If message doesn't contain one/more of them, the empty strings will be returned.
    """
    Date = ""
    if origin.has_key("date"): Date = origin["date"].strip()
    From = ""
    if origin.has_key("from"): From = origin["from"].strip()
    To = ""
    if origin.has_key("to"): To = origin["to"].strip()
    Subject = ""
    if origin.has_key("subject"): Subject = origin["subject"].strip()
    return From, To, Subject, Date

def confirmInput(s):
    print (s)

def getmailcontent(file):
    # msg = email.message_from_file(open('sample.eml'))
    with open(file, 'rb') as fp:
        msg = BytesParser(policy=policy.default).parse(fp)

    text = msg.get_body(preferencelist=('plain')).get_content()
    return text

if __name__ == '__main__':

    test = 'YUlRsXUXGqKvQBCK3MKHJ26zj08DWETbeYs4OhLKtPe8d1rzo5RU0ThsN9z/qBE3P70G7v/zUnbJDBO0DvtuFOYcbjtmwbP+dd0R5R06nw0PBHAz0dA2MaWU3J/ZQemA1mG1AS+xN9oj8CZ5Tt2c/nOOUTOWxYZh8z6VdYm7A/nhRJp2jSF0pErDwsZX6xcupFku0XfbaN9CUbhvVtMVVIFRizNYOA8jxQvWhzyinLyEsJoFRgaOREDGlFUaJNTpLd8cskkHGRTmnQqMsdbyD1U5kTINR0Y0GbMYd3L6KPkl228uMZRxQd5wN6HhbrBbNllAH57HnBarnuRvuWONkKbKLp1lrE/SF/Lhca7PfsjcGUFQfMqACHmF24ICOL7ltYQVuIY69nYXv8mT9/F+OB5f/cx1DqHRGdr2bVMU0P3j4YnNuwR7Z/mtwppHGnn46eNIGulW5VPhwS8vFVI8mgGSB9pjy8DfltjzH5+J8Mprek1J2UqXNicHmGic20R/Cj46yFN0GRc44wR1ZwINhMKcgTk3nKXOEDtNkqA9oZ3nZ7E='

    result = base64.b64decode(test)
    print (result)

import sys
import os
import io
import traceback
import inspect
import time
import datetime
import iso8601 # pip install iso8601
import regex


def get_callername():
    framelist= inspect.stack()
    try:
        return framelist[2].function
    finally:
        del framelist


def get_exception(ex):
    exc_buffer = io.StringIO()
    traceback.print_exc(file=exc_buffer)
    msg= exc_buffer.getvalue()
    msg= regex.sub(r'[\r\n]', '|', msg)
    return msg



def removeindents(txt):
    txt= regex.sub(r'^[\s]+','',txt)
    txt= regex.sub(r'\n[\s]+',' ',txt)
    txt= regex.sub(r'\n$','',txt)
    return txt



def format_ts(ts):
    if ts == None: return None
    return ts.strftime('%Y-%m-%d %H:%M:%S.%f %z')



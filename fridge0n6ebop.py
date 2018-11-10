#!/usr/local/bin/python
# encoding=utf8


import requests
import logging
import json
rlogger = logging.getLogger('fridge')
# ch = logging.StreamHandler()
# logger.setLevel('debug')
# rlogger.addHandler(ch)


class FreezeRequest(object):
    def __init__(self, requests_data, handle_func=None, logger=None):
        '''
        requests_data：dict, like:
        {
        'url': 'www.baidu.com',
        'method': 'POST',
        'kwargs': {
                'data': {'screenshot': False, 'xpath': []},
                'timeout': 6,
            }
        }
        '''
        self.requests_data = requests_data
        self.url = self.requests_data.get('url')
        self.method = self.requests_data.get('method')
        self.kwargs = self.requests_data.get('kwargs')
        self.timeout = self.requests_data.get('timeout', 5)
        self.msg = ''
        self.code = 0
        self.data = None
        self.logger = logger or rlogger
        self._handle = handle_func

    def go(self):
        try:
            rsp = requests.request(self.method, self.url, **self.kwargs)
        except Exception as e:
            self.msg = 'error when requests api, fail with %s' % e
            self.code = -1
            self.logger.error(self.msg)
            return self.return_()

        if rsp.status_code != 200:
            self.msg = 'error with wrong requests status code : %s. content: %s' % (rsp.status_code, rsp.content)
            self.code = -1
            self.logger.error(self.msg)
            return self.return_()

        try:
            self.data = json.loads(rsp.content)
        except Exception as e:
            self.msg = 'error when json load content: %s, content: %s' % (e, rsp.content[:100])
            self.code = -1
            self.logger.error(self.msg)
            return self.return_()

        if self._handle:
            try:
                self.data = self._handle(self.data)
            except Exception as e:
                self.msg = 'error when handle_func: %s' % e
                self.code = -1
                self.logger.error(self.msg)
                return self.return_()

        return self.return_()

    def return_(self):
        return {
                'code': self.code,
                'msg': self.msg,
                'data': self.data
                }

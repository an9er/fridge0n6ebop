#!/usr/local/bin/python
# encoding=utf8


import logging
logger = logging.getLogger('fridge')
ch = logging.StreamHandler()
# ch.setLevel('DEBUG')
logger.addHandler(ch)

def case1():
    print 'ca 1:w '


def case2(a):
    '''
    eg: python test.py case2 "{'a': 1}"
    '''
    print a

def case3():
    from fridge0n6ebop import FreezeRequest
    rdata = {
            'url': 'https://jsonplaceholder.typicode.com/todos/1',
            'method': 'GET',
            'kwargs': {
                # 'data': {'screenshot': False, 'xpath': []},
                'timeout': 6}
            }
    frequest = FreezeRequest(rdata)
    print frequest.go()

if __name__ == '__main__':
    import sys
    la = len(sys.argv)
    if la == 1:
        exit()

    if la == 2:
        func = sys.argv[1]
        globals()[func]()
    elif la == 3:
        func = sys.argv[1]
        arg = sys.argv[2]
        globals()[func](eval(arg))

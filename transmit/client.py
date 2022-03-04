#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'hbh112233abc@163.com'

import json
from typing import Callable

from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol

from trans import Transmit


class Client(object):
    def __init__(self, host='127.0.0.1', port=8000):
        self.host = host
        self.port = port
        self.func = ''
        self.transport = TSocket.TSocket(self.host, self.port)
        self.transport = TTransport.TBufferedTransport(self.transport)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Transmit.Client(protocol)

    def __enter__(self):
        self.transport.open()
        return self

    def _exec(self, data:dict):
        json_string = json.dumps(data)
        res = self.client.invoke(self.func, json_string)
        return res

    def __getattr__(self, __name: str) -> Callable:
        self.func = __name
        return self._exec

    def __exit__(self, exc_type, exc_value, trace):
        self.transport.close()

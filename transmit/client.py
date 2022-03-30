#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'hbh112233abc@163.com'

import json
from typing import Callable

import pretty_errors
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol

from .trans import Transmit
from .tool import get_logger

class Client(object):
    def __init__(self, host='127.0.0.1', port=8000):
        self.host = host
        self.port = port
        self.log = get_logger()
        self.func = ''
        self.transport = TSocket.TSocket(self.host, self.port)
        self.transport = TTransport.TBufferedTransport(self.transport)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Transmit.Client(protocol)

    def __enter__(self):
        self.transport.open()
        self.log.info(f"CONNECT SERVER {self.host}:{self.port}")
        return self

    def _exec(self, data:dict):
        try:
            self.log.info(f'----- CALL {self.func} -----')
            self.log.info(f'----- PARAMS BEGIN -----')
            self.log.info(data)
            self.log.info(f'----- PARAMS END -----')
            json_string = json.dumps(data)
            res = self.client.invoke(self.func, json_string)
            self.log.info(f'----- RESULT -----')
            self.log.info(f"\n{res}")
            return res
        except Exception as e:
            self.log.exception(e)
        finally:
            self.log.info(f'----- END {self.func} -----')

    def __getattr__(self, __name: str) -> Callable:
        self.func = __name
        return self._exec

    def __exit__(self, exc_type, exc_value, trace):
        self.transport.close()
        self.log.info(f"DISCONNECT SERVER {self.host}:{self.port}")

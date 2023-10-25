#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "hbh112233abc@163.com"


import json
from typing import Callable

import pretty_errors
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol

from .trans import Transmit
from .log import logger


class Client(object):
    def __init__(self, host="127.0.0.1", port=8000):
        self.host = host
        self.port = port
        self.log = logger
        self.func = ""
        self.transport = TSocket.TSocket(self.host, self.port)
        self.transport = TTransport.TBufferedTransport(self.transport)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Transmit.Client(protocol)

    def __enter__(self):
        self.transport.open()
        self.log.info(f"CONNECT SERVER {self.host}:{self.port}")
        return self

    def _exec(self, data: dict):
        try:
            self.log.info(f"----- CALL {self.func} -----")
            self.log.info(f"----- PARAMS BEGIN -----")
            self.log.info(data)
            if not isinstance(data, dict):
                raise TypeError("params must be dict")
            params = json.dumps(data)
            self.log.info(f"----- PARAMS END -----")
            res = self.client.invoke(self.func, params)
            self.log.info(f"----- RESULT -----")
            self.log.info(f"\n{res}")
            result = json.loads(res)
            if result["code"] != 0:
                raise Exception(f"{result['code']}: {result['msg']}")
            return result.get("data")
        except Exception as e:
            self.log.exception(e)
            raise e
        finally:
            self.log.info(f"----- END {self.func} -----")

    def __getattr__(self, __name: str) -> Callable:
        self.func = __name
        return self._exec

    def __exit__(self, exc_type, exc_value, trace):
        self.transport.close()
        self.log.info(f"DISCONNECT SERVER {self.host}:{self.port}")

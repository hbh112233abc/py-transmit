#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "hbh112233abc@163.com"


import json
import time
from typing import Callable

import pretty_errors
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol

from .trans import Transmit
from .log import logger


class Client(object):
    def __init__(self, host: str = "127.0.0.1", port: int = 8000, debug: bool = False):
        self.host = host
        self.port = port
        self.log = logger
        self.debug = debug
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
            if not isinstance(data, dict):
                raise TypeError("params must be dict")

            self.log.info(f"----- CALL {self.func} -----")

            if self.debug:
                self.log.info(f"----- PARAMS BEGIN -----")
                self.log.info(data)
                self.log.info(f"----- PARAMS END -----")
                t = time.time()

            params = json.dumps(data)
            res = self.client.invoke(self.func, params)

            if self.debug:
                self.log.info(f"----- RESULT -----")
                self.log.info(f"\n{res}")
                self.log.info(f"----- USED {time.time() - t:.2f} s -----")

            result = json.loads(res)
            if result["code"] != 0:
                raise Exception(f"{result['code']}: {result['msg']}")
            return result.get("data")
        except Exception as e:
            self.log.error(e)
            raise e
        finally:
            self.log.info(f"----- END {self.func} -----")

    def __getattr__(self, __name: str) -> Callable:
        self.func = __name
        return self._exec

    def __exit__(self, exc_type, exc_value, trace):
        self.transport.close()
        self.log.info(f"DISCONNECT SERVER {self.host}:{self.port}")

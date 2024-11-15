#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "hbh112233abc@163.com"

import json
import time
from typing import Callable

from loguru import logger
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol

from .util import Result
from .trans import Transmit


class Client(object):
    def __init__(self, host: str = "127.0.0.1", port: int = 8000, debug: bool = False):
        self.host = host
        self.port = port
        self.debug = debug
        self.func = ""
        self.transport = TSocket.TSocket(self.host, self.port)
        self.transport = TTransport.TBufferedTransport(self.transport)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Transmit.Client(protocol)

    def __enter__(self):
        self.transport.open()
        logger.info(f"CONNECT SERVER {self.host}:{self.port}")
        return self

    def _exec(self, data: dict):
        try:
            if not isinstance(data, dict):
                raise TypeError("params must be dict")

            logger.info(f"----- CALL {self.func} -----")

            if self.debug:
                logger.info(f"----- PARAMS BEGIN -----")
                logger.info(data)
                logger.info(f"----- PARAMS END -----")
                t = time.time()

            params = json.dumps(data)
            res = self.client.invoke(self.func, params)

            if self.debug:
                logger.info(f"----- RESULT -----")
                logger.info(f"\n{res}")
                logger.info(f"----- USED {time.time() - t:.2f} s -----")

            result = Result.model_validate_json(res)
            if result.code != 0:
                raise Exception(f"{result.code}: {result.msg}")
            return result.data
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            logger.info(f"----- END {self.func} -----")

    def __getattr__(self, __name: str) -> Callable:
        self.func = __name
        return self._exec

    def __exit__(self, exc_type, exc_value, trace):
        self.transport.close()
        logger.warning(f"DISCONNECT SERVER {self.host}:{self.port}")

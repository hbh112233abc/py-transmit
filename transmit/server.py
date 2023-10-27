#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "hbh112233abc@163.com"

import argparse
import json
import signal
import sys
import time
from typing import Any

import pretty_errors
from pydantic import BaseModel

from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from transmit.trans import Transmit
from transmit.log import logger


class Result(BaseModel):
    code: int = 0
    msg: str = ""
    data: Any = None


class Server:
    def __init__(self, port: int = 0, host: str = ""):
        self.log = logger

        parser = argparse.ArgumentParser(description="Thrift Server")
        parser.add_argument("--host", type=str, default="0.0.0.0", help="host")
        parser.add_argument("--port", type=int, default=8000, help="port")
        parser.add_argument("--debug", type=bool, default=False, help="debug mode")

        args = parser.parse_args()
        self.host = host if host else args.host
        self.port = port if port else args.port
        self.debug = args.debug

    def run(self):
        # 创建Thrift服务处理器
        processor = Transmit.Processor(self)

        # 创建TSocket
        transport = TSocket.TServerSocket(self.host, self.port)

        # 创建传输方式
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        # 创建线程池服务器
        server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
        self.log.info(f"START SERVER {self.host}:{self.port}")

        server.serve()

    def invoke(self, func, data):
        try:
            if not getattr(self, func):
                raise Exception(f"{func} not found")

            self.log.info(f"----- CALL {func} -----")

            params = json.loads(data)
            if not isinstance(params, dict):
                raise Exception("params must be dict json")

            if self.debug:
                self.log.info(f"----- PARAMS BEGIN -----")
                self.log.info(params)
                self.log.info(f"----- PARAMS END -----")
                self.log.info(f"----- START {func} -----")
                t = time.time()

            result = getattr(self, func)(**params)

            if self.debug:
                self.log.info(result)
                self.log.info(f"----- USED {time.time() - t:.2f}s -----")

            return self._success(result)
        except Exception as e:
            self.log.exception(e)
            return self._error(str(e))
        finally:
            self.log.info(f"----- END {func} -----")

    def _error(self, msg: str = "error", code: int = 1) -> str:
        """Error return

        Args:
            msg (str, optional): result message. Defaults to 'error'.
            code (int, optional): result code. Defaults to 1.

        Returns:
            str: json string
        """
        result = Result(code=code, msg=msg)
        self.log.error(f"ERROR:{result}")
        return result.model_dump_json(indent=2)

    def _success(self, data={}, msg: str = "success", code: int = 0) -> str:
        """Success return

        Args:
            data (dict, optional): result data. Default to {}.
            msg (str, optional): result message. Defaults to 'success'.
            code (int, optional): result code. Defaults to 0.

        Returns:
            str: 成功信息json字符串
        """
        result = Result(
            code=code,
            msg=msg,
            data=data,
        )
        self.log.info(f"SUCCESS:{result}")
        return result.model_dump_json(indent=2)


if __name__ == "__main__":
    Server().run()

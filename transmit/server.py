#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "hbh112233abc@163.com"

import signal
import time
import json
import argparse
from typing import Literal

from loguru import logger
from thrift.server import TServer
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from thrift.server.TProcessPoolServer import TProcessPoolServer

from .util import Result
from .trans import Transmit


class Server:
    def __init__(
        self,
        port: int = 0,
        host: str = "",
        workers: int = 0,
        server_type: Literal["", "thread", "process"] = "",
    ):
        parser = argparse.ArgumentParser(description="Thrift Server")
        parser.add_argument("--host", type=str, default="0.0.0.0", help="host")
        parser.add_argument("--port", type=int, default=8000, help="port")
        parser.add_argument("--workers", type=int, default=3, help="workers")
        parser.add_argument(
            "--type",
            type=str,
            choices=["thread", "process"],
            default="thread",
            help="server type one of `thread`,`process`",
        )
        parser.add_argument("--debug", type=bool, default=False, help="debug mode")

        args = parser.parse_args()
        self.host = host if host else args.host
        self.port = port if port else args.port
        self.workers = workers if workers else args.workers
        self.server_type = server_type if server_type else args.type
        self.debug = args.debug

    def run(self):
        # 创建Thrift服务处理器
        processor = Transmit.Processor(self)
        # 创建TSocket
        transport = TSocket.TServerSocket(self.host, self.port)
        # 创建传输方式
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        try:
            if self.server_type == "thread":
                # 创建线程池服务器
                server = TServer.TThreadPoolServer(
                    processor, transport, tfactory, pfactory, daemon=True
                )
                server.setNumThreads(self.workers)

                # 捕获SIGINT信号
                def signal_handler(signal, frame):
                    print("You pressed Ctrl+C!")
                    server.stop()

                signal.signal(signal.SIGINT, signal_handler)
            elif self.server_type == "process":
                # 创建进程池服务器
                server = TProcessPoolServer(processor, transport, tfactory, pfactory)
                server.setNumWorkers(self.workers)

            logger.info(
                f"START [{self.workers}] {self.server_type.capitalize()} Server {self.host}:{self.port}"
            )

            server.serve()

        except Exception as e:
            logger.exception(e)

    def invoke(self, func, data):
        try:
            if not getattr(self, func):
                raise Exception(f"{func} not found")

            logger.info(f"----- CALL {func} -----")

            params = json.loads(data)
            if not isinstance(params, dict):
                raise Exception("params must be dict json")

            if self.debug:
                logger.info(f"----- PARAMS BEGIN -----")
                logger.info(params)
                logger.info(f"----- PARAMS END -----")
                logger.info(f"----- START {func} -----")
                t = time.time()

            result = getattr(self, func)(**params)

            if self.debug:
                logger.info(result)
                logger.info(f"----- USED {time.time() - t:.2f}s -----")

            return self._success(result)
        except Exception as e:
            logger.exception(e)
            return self._error(str(e))
        finally:
            logger.info(f"----- END {func} -----")

    def _error(self, msg: str = "error", code: int = 1) -> str:
        """Error return

        Args:
            msg (str, optional): result message. Defaults to 'error'.
            code (int, optional): result code. Defaults to 1.

        Returns:
            str: json string
        """
        result = Result(code=code, msg=msg)
        logger.error(f"ERROR:{result}")
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
        logger.info(f"SUCCESS:{result}")
        return result.model_dump_json(indent=2)


if __name__ == "__main__":
    Server().run()

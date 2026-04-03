#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "hbh112233abc@163.com"

import os
import sys
import time
import json
import signal
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
    """Thrift服务器基类

    注意:
    - 使用进程池模式时，handler 必须是可序列化的
    - 避免在 handler 中持有不可序列化的状态（如文件句柄、锁等）
    """

    def __init__(
        self,
        port: int = 0,
        host: str = "",
        workers: int = 0,
        server_type: Literal["", "thread", "process"] = "",
    ):
        self._shutdown = False
        parser = argparse.ArgumentParser(description="Thrift Server")
        # 读取环境变量作为parser的默认值
        env_host = os.getenv("HOST", "0.0.0.0")
        try:
            env_port = int(os.getenv("PORT", "8000"))
        except (ValueError, TypeError):
            env_port = 8000

        try:
            env_workers = int(os.getenv("WORKERS", "3"))
        except (ValueError, TypeError):
            env_workers = 3
        env_server_type = os.getenv("SERVER_TYPE", "thread")
        env_debug = os.getenv("DEBUG", "False") in ("True", "true", "1")

        parser.add_argument("--host", type=str, default=env_host, help="host")
        parser.add_argument("--port", type=int, default=env_port, help="port")
        parser.add_argument("--workers", type=int, default=env_workers, help="workers")
        parser.add_argument(
            "--type",
            type=str,
            choices=["thread", "process"],
            default=env_server_type,
            help="server type one of `thread`,`process`",
        )
        parser.add_argument("--debug", type=bool, default=env_debug, help="debug mode")
        # pytest 环境检测：如果 pytest 已加载到 sys.modules 中，说明正在运行测试
        if "pytest" in sys.modules:
            args = parser.parse_args(args=[])
        else:
            args = parser.parse_args()

        self.host = host if host else args.host
        self.port = port if port else args.port
        self.workers = workers if workers else args.workers
        self.server_type = server_type if server_type else args.type
        self.debug = args.debug

        # 确保类型正确
        if not isinstance(self.workers, int) or self.workers < 1:
            raise ValueError("workers must be a positive integer")

        # 服务初始化
        self.server_init()

        # 注册信号处理
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def server_init(self):
        # 创建Thrift服务处理器
        processor = Transmit.Processor(self)
        # 创建TSocket
        self.transport = TSocket.TServerSocket(self.host, self.port)
        # 创建传输方式
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        if self.server_type == "thread":
            # 创建线程池服务器
            self.server = TServer.TThreadPoolServer(
                processor, self.transport, tfactory, pfactory, daemon=True
            )
            self.server.setNumThreads(self.workers)

        elif self.server_type == "process":
            # 创建进程池服务器
            # 注意：确保 handler 类及其属性是可序列化的
            self.server = TProcessPoolServer(
                processor, self.transport, tfactory, pfactory
            )
            self.server.setNumWorkers(self.workers)

        return self.server

    def signal_handler(self, signum, frame):
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.server.stop()
        self._shutdown = True

    def run(self):
        try:
            logger.info(
                f"START [{self.workers}] {self.server_type.capitalize()} Server {self.host}:{self.port}"
            )
            self.server.serve()
        except Exception as e:
            logger.exception(e)
        finally:
            # 确保正确关闭传输层资源
            try:
                if hasattr(self.server.serverTransport, "close"):
                    self.server.serverTransport.close()
            except Exception as e:
                logger.warning(f"Failed to close transport: {e}")

    def invoke(self, func, data):
        try:
            # 防止调用私有方法和特殊方法
            if func.startswith("_"):
                raise Exception(f"Forbidden method: {func}")

            if not getattr(self, func):
                raise Exception(f"{func} not found")

            logger.info(f"----- CALL {func} -----")

            params = json.loads(
                data, parse_constant=lambda x: None
            )  # 防止 NaN/Infinity
            # 验证 JSON 深度和大小
            if len(data) > 100 * 1024 * 1024:  # 100MB 限制
                raise Exception("JSON data too large")
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

    def ping(self) -> dict:
        """
        健康检查方法，供 Docker 健康检查使用
        """
        return "pong"

    def _error(self, msg: str = "error", code: int = 1) -> str:
        """Error return

        Args:
            msg (str, optional): result message. Defaults to 'error'.
            code (int, optional): result code. Defaults to 1.

        Returns:
            str: json string
        """
        result = Result.error(msg, code)
        logger.error(f"ERROR:{result}")
        return result.model_dump_json(indent=2)

    def _success(self, data: dict = None, msg: str = "success", code: int = 0) -> str:
        """Success return

        Args:
            data (dict, optional): result data. Default to None.
            msg (str, optional): result message. Defaults to 'success'.
            code (int, optional): result code. Defaults to 0.

        Returns:
            str: 成功信息json字符串
        """
        if data is None:
            data = {}
        result = Result.success(data, msg, code)
        logger.debug(f"SUCCESS:{result}")
        return result.model_dump_json(indent=2)


if __name__ == "__main__":
    Server().run()

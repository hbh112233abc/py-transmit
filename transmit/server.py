#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'hbh112233abc@163.com'

import json
import pretty_errors

from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from .trans import Transmit
from .tool import get_logger


class Server:
    def __init__(self, port=8000, host='0.0.0.0'):
        self.port = port
        self.host = host
        self.log = get_logger()

    def run(self):
        processor = Transmit.Processor(self)
        transport = TSocket.TServerSocket(self.host, self.port)
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()
        server = TServer.TThreadPoolServer(processor, transport, tfactory,
                                           pfactory)
        self.log.info(f'START SERVER {self.host}:{self.port}')
        server.serve()

    def invoke(self, func, data):
        try:
            if not getattr(self, func):
                raise Exception(f'{func} not found')
            self.log.info(f'----- CALL {func} -----')
            params = json.loads(data)

            self.log.info(f'----- PARAMS BEGIN -----')
            self.log.info(params)
            self.log.info(f'----- PARAMS END -----')

            result = getattr(self, func)(**params)
            return self._success(result)
        except Exception as e:
            self.log.exception(e)
            return self._error(str(e))
        finally:
            self.log.info(f'----- END {func} -----')


    def _error(self, msg:str='error', code:int=1, **kw)->str:
        """Error return

        Args:
            msg (str, optional): result message. Defaults to 'error'.
            code (int, optional): result code. Defaults to 1.

        Returns:
            str: json string
        """
        result = {
            'code': code,
            'msg': msg,
        }
        if kw:
            result.update(kw)
        self.log.error(f'ERROR:{result}')
        return json.dumps(result)

    def _success(self, data={}, msg:str='success', code:int=0, **kw)->str:
        """Success return

        Args:
            data (dict, optional): result data. Default to {}.
            msg (str, optional): result message. Defaults to 'success'.
            code (int, optional): result code. Defaults to 0.

        Returns:
            str: 成功信息json字符串
        """
        result = {
            'code': code,
            'msg': msg,
            'data': data,
        }
        if kw:
            result.update(kw)
        self.log.info(f'SUCCESS:{result}')
        return json.dumps(result, ensure_ascii=False, indent=True)

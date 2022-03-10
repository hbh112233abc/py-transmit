#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'hbh112233abc@163.com'

import json

from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from .trans import Transmit


class Server:
    def __init__(self, port=8000, host='0.0.0.0'):
        self.port = port
        self.host = host

    def run(self):
        processor = Transmit.Processor(self)
        transport = TSocket.TServerSocket(self.host, self.port)
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()
        server = TServer.TThreadPoolServer(processor, transport, tfactory,
                                           pfactory)
        print(f'start python server {self.host}:{self.port}')
        server.serve()

    def invoke(self, func, data):
        try:
            if not getattr(self, func):
                raise Exception(f'{func} not found')

            params = json.loads(data)
            result = getattr(self, func)(**params)
            return self._success(result)
        except Exception as e:
            return self._error(str(e))


    def _error(self, msg:str='error', code:int=0, **kw)->str:
        """Error return

        Args:
            msg (str, optional): result message. Defaults to 'error'.
            code (int, optional): result code. Defaults to 0.

        Returns:
            str: json string
        """
        result = {
            'code': code,
            'msg': msg,
        }
        if kw:
            result.update(kw)
        print(f'error:{result}')
        return json.dumps(result)

    def _success(self, data={}, msg:str='success', code:int=1, **kw)->str:
        """Success return

        Args:
            data (dict, optional): result data. Default to {}.
            msg (str, optional): result message. Defaults to 'success'.
            code (int, optional): result code. Defaults to 1.

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
        print(f'success:{result}')
        return json.dumps(result, ensure_ascii=False, indent=True)

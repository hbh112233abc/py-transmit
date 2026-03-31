#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Docker 健康检查脚本，通过 Thrift Client 调用 ping 方法检测服务状态"""

import os
import sys
import argparse
from transmit.client import Client

parser = argparse.ArgumentParser()
parser.add_argument(
    "--host", default=os.getenv("HOST", "127.0.0.1"), help="Service host"
)
parser.add_argument(
    "--port", default=int(os.getenv("PORT", "8000")), type=int, help="Service port"
)
args = parser.parse_args()
host = args.host
port = args.port
try:
    with Client(host=host, port=port, debug=True) as client:
        client.ping({})
    sys.exit(0)
except Exception:
    sys.exit(1)

#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "hbh112233abc@163.com"

# 未能成功实现对接服务端

import socket
import struct

# 定义 Thrift 协议类型常量
T_BINARY_PROTOCOL = 0

# 创建一个 Socket 连接
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("127.0.0.1", 18100)  # 服务端地址和端口
sock.connect(server_address)

try:
    # 发送请求头
    # 协议类型 TBinaryProtocol
    # 方法名长度和方法名
    method_name = "test_function"
    method_name_len = len(method_name)
    request_header = struct.pack(
        "!B%dsB" % method_name_len, T_BINARY_PROTOCOL, method_name.encode(), 0
    )

    # 发送请求头
    sock.sendall(request_header)

    # 接收响应头
    response_header = sock.recv(4)  # 4 字节的响应头长度
    header_len = struct.unpack("!I", response_header)[0]

    # 接收响应数据
    response_data = sock.recv(header_len)

    # 解析响应数据
    response_protocol_type, response_method_name_len = struct.unpack(
        "!B%ds" % header_len, response_data
    )
    # response_method_name = response_method_name.decode()

    # 根据协议类型来解析响应
    if response_protocol_type == T_BINARY_PROTOCOL:
        # TBinaryProtocol 格式
        response_data = sock.recv(4)  # 4 字节的数据长度
        data_len = struct.unpack("!I", response_data)[0]
        response_data = sock.recv(data_len)  # 实际数据

        # 反序列化响应
        print(response_data)
        # result = ExampleStruct()
        # result.read(response_data)

        # print(f"Received value from server: {result.value}")
    else:
        print("Unsupported protocol type")

finally:
    sock.close()

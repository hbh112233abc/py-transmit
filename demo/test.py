#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "hbh112233abc@163.com"

from multiprocessing import Condition, Process, process
import queue
import select
import signal
import socket
import sys
import threading
from time import sleep

from loguru import logger

clients = queue.Queue()

HOST = "127.0.0.1"
PORT = 18100


def serveClient(client):
    """Process input/output from a client for as long as possible"""
    try:
        while True:
            client_socket, client_address = client
            print("client address:", client_address)
            data = client_socket.recv(1024)
            msg = "RECV:" + data.decode()
            client_socket.sendall(msg.encode())
    except Exception as x:
        logger.exception(x)
    finally:
        client_socket.close()


def serveThread():
    """Loop around getting clients from the shared queue and process them."""
    while True:
        try:
            client = clients.get()
            serveClient(client)
        except Exception as x:
            logger.exception(x)


def serve():
    """Start a fixed number of worker threads and put client into a queue"""

    threads = 3
    for i in range(threads):
        try:
            t = threading.Thread(target=serveThread)
            t.daemon = True
            t.start()
        except Exception as x:
            logger.exception(x)

    # Pump the socket for clients
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)  # 服务端地址和端口
    sock.bind(server_address)
    sock.listen(1)
    print(f"Server:{server_address[0]}:{server_address[1]}")
    while True:
        try:
            client = sock.accept()
            print(client)
            if not client:
                continue
            clients.put(client)
        except Exception as x:
            logger.exception(x)


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)  # 服务端地址和端口
    sock.connect(server_address)
    try:
        sock.sendall("hello".encode())
        res = sock.recv(1024)
        print(res)
    finally:
        sock.close()


def start_server():
    w = Process(target=serve)
    w.daemon = True
    w.start()
    stopCondition = Condition()
    while True:
        stopCondition.acquire()
        try:
            stopCondition.wait()
            break
        except (SystemExit, KeyboardInterrupt):
            break
        except Exception as x:
            logger.exception(x)


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        client()
    else:
        start_server()

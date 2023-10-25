# 示例说明

## 运行服务端

```shell
python -m demo.server
```

> 启动服务

```shell
2023-10-25 16:34:04.483 | INFO     | transmit.log:<module>:30 - SYSTEM:Windows-10-10.0.19043-SP0
2023-10-25 16:34:04.489 | INFO     | transmit.log:<module>:31 - PYTHON:3.9.7 (tags/v3.9.7:1016ef3, Aug 30 2021, 20:19:38) [MSC v.1929 64 bit
v.1929 64 bit (AMD64)]
2023-10-25 16:34:04.490 | INFO     | transmit.log:<module>:32 - LOG: D:\py\transmit\demo\log [INFO]
2023-10-25 16:34:04.544 | INFO     | transmit.server:run:37 - START SERVER 0.0.0.0:18100
```

> 处理请求

```shell
2023-10-25 16:34:43.958 | INFO     | transmit.server:invoke:44 - ----- CALL test_function -----
2023-10-25 16:34:43.959 | INFO     | transmit.server:invoke:49 - ----- PARAMS BEGIN -----
2023-10-25 16:34:43.960 | INFO     | transmit.server:invoke:50 - {'msg': 'hello world'}
2023-10-25 16:34:43.961 | INFO     | transmit.server:invoke:51 - ----- PARAMS END -----
Testing: hello world
2023-10-25 16:34:43.962 | INFO     | transmit.server:_success:110 - SUCCESS:code=0 msg='success' data={'say': 'Happy everyday!!!'}
2023-10-25 16:34:43.963 | INFO     | transmit.server:invoke:59 - ----- END test_function -----
```

## 运行客户端

```shell
python -m demo.client
```

> 请求结果

```shell
2023-10-25 16:34:43.936 | INFO     | transmit.log:<module>:30 - SYSTEM:Windows-10-10.0.19043-SP0
2023-10-25 16:34:43.942 | INFO     | transmit.log:<module>:31 - PYTHON:3.9.7 (tags/v3.9.7:1016ef3, Aug 30 2021, 20:19:38) [MSC
v.1929 64 bit (AMD64)]
2023-10-25 16:34:43.944 | INFO     | transmit.log:<module>:32 - LOG: D:\py\transmit\demo\log [INFO]
2023-10-25 16:34:43.949 | INFO     | transmit.client:__enter__:30 - CONNECT SERVER 127.0.0.1:18100
2023-10-25 16:34:43.951 | INFO     | transmit.client:_exec:35 - ----- CALL test_function -----
2023-10-25 16:34:43.953 | INFO     | transmit.client:_exec:36 - ----- PARAMS BEGIN -----
2023-10-25 16:34:43.956 | INFO     | transmit.client:_exec:37 - {'msg': 'hello world'}
2023-10-25 16:34:43.957 | INFO     | transmit.client:_exec:41 - ----- PARAMS END -----
2023-10-25 16:34:43.965 | INFO     | transmit.client:_exec:43 - ----- RESULT -----
2023-10-25 16:34:43.966 | INFO     | transmit.client:_exec:44 -
{
  "code": 0,
  "msg": "success",
  "data": {
    "say": "Happy everyday!!!"
  }
}
2023-10-25 16:34:43.967 | INFO     | transmit.client:_exec:53 - ----- END test_function -----
<class 'dict'>
{'say': 'Happy everyday!!!'}
2023-10-25 16:34:43.970 | INFO     | transmit.client:__exit__:61 - DISCONNECT SERVER 127.0.0.1:18100
```

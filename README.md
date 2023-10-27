# Transmit Server & Client

## Install

```
pip install transmit
```

## Usage

### Server

```
from transmit.server import Server

class TestServer(Server):
    def __init__(self,port=18100):
        super().__init__(port)

    def test_function(self,msg):
        print('Testing:',msg)
        return {"say":"Happy everyday!!!"}

if __name__ == '__main__':
    ts = TestServer()
    ts.run()

```

> Result

```shell
START SERVER 0.0.0.0:18100

```

#### Success Response

```
{
    "code":1,
    "msg":"success",
    "data":"handle result data. AnyType"
}
```

#### Error Response

```
{
    "code":0,
    "msg":"error message",
    "data":null
}
```

### Client

```
from transmit.client import Client

with Client("127.0.0.1",18100) as c:
    result = c.test_function({"msg":"hello world"})
    print(type(result))
    print(result)

```

> Result

```shell
> <class 'dict'>
> {'say': 'Happy everyday!!!'}
```

### Advanced Usage

1. debug mode

debug mode will print and log all request and response data.

```shell
# debug server
> python test_server.py --debug 1
```

```python
# debug client
with Client("127.0.0.1",18100,debug=True) as c:
    ...
```

2. server cli setting

```shell
> python test_server.py --host "127.0.0.1" --port 3000 --debug 1
```

### Refs

[Thrift](https://thrift.apache.org/)

```

```

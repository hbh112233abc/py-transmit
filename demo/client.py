from transmit.client import Client

with Client("127.0.0.1", 18100) as c:
    result = c.test_function({"msg": "hello world"})
    print(type(result))
    print(result)

    error = c.error_function({"age": "haha"})
    print(error)

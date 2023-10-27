from transmit.server import Server


class TestServer(Server):
    def __init__(self, port=18100):
        super().__init__(port)

    def test_function(self, msg):
        print("Testing:", msg)
        return {"say": "Happy everyday!!!"}

    def error_function(self, age: int):
        print("Error:", age)
        return age + 1


if __name__ == "__main__":
    ts = TestServer()
    ts.run()

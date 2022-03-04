from server import Server

class TestServer(Server):
    def __init__(self,port=18100):
        super().__init__(port)

    def test_function(self,msg):
        print('Testing:',msg)
        return {"say":"Happy everyday!!!"}

if __name__ == '__main__':
    ts = TestServer()
    ts.run()

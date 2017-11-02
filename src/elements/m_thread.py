import threading
from socket import *

class MSocket(threading.Thread):
    def __init__(self, port, execute):
        super().__init__(name="wtc_sock")
        self.exer = execute
        self.ip = '127.0.0.1'
        self.port = int(port)
        self.start()
        self.exer.execute()

    def run(self):
        #打开连接
        address = (self.ip, self.port)
        sock = socket(AF_INET, SOCK_STREAM)
        print(sock, address)
        sock.bind(address)
        sock.listen(10)
        while True:
            try:
                tcpClientSock, addr = sock.accept()
                # sockThread(tcpClientSock) tuple元组只有一个元素的时候需要在后面加一个逗号，防止歧义。
                threading.Thread(target=self.sock_work, args=(tcpClientSock,)).start()
            except:
                pass
        sock.close()

# 协议 video*文件全路径
    def sock_work(self,tcpClientSock):
        try:
            data = tcpClientSock.recv(1024)
            if data.decode('utf-8') > "video":
                resp = self.exer.getVideoLengthAndTranslate(data.decode('utf-8').split('*')[1]).encode('utf8')
                print(data, '    ', resp)
                tcpClientSock.send(resp)

        except Exception as e:
            print(e)
        finally:
            tcpClientSock.close()
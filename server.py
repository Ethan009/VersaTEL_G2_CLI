#coding:utf-8
import socketserver,socket,subprocess,timeit

host_port = 12129
# host_ip = "192.168.36.61"
host_ip = "10.203.1.198"
byteData = b'null'
start = 0

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global byteData
        self.request.send(('%s connection succeeded' % h).encode())
        while True:
            data = self.request.recv(4096).decode()
            global start
            print ('recv:',data)
            if data=='exit':
                break
            elif 'CLIcommands' in data:
                start = timeit.timeit()
                subprocess.getoutput('python3 vtel.py stor gui -db')
                self.request.sendall(byteData)
            elif 'database' in data:
                end = timeit.timeit()
                print('time')
                print(end-start)
                self.request.send(b'ok')
                sql_script = self.request.recv(8192)
                byteData = sql_script
                self.request.send(b'over')
            else:
                pass





if __name__ == '__main__':
    h, p = host_ip,host_port
    server = socketserver.ThreadingTCPServer((h, p), MyTCPHandler)
    server.serve_forever()

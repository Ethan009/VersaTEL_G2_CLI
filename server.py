#coding:utf-8
import socketserver,socket,subprocess

host_port = 12129
host_ip = "192.168.36.61"
# host_ip = "10.203.1.198"
byteData = b'null'

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
                subprocess.getoutput('python3 vtel.py stor gui -db')
                data_len = str(len(byteData))
                print(byteData)
                self.request.sendall(data_len.encode())
                self.request.recv(8192)
                self.request.sendall(byteData)
            elif 'database' in data:
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
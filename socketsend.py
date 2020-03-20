import socket,pickle
import linstordb
from stor_cmds import Action as stor_action

ip_port = ('192.168.36.61',12129)

class SocketSend():
    def __init__(self):
        self.client = socket.socket()
        self.client.connect(ip_port)

    def sql_script(self,*args):
        db = linstordb.LINSTORDB()
        return db.data_base_dump()

    def print_sql(self,func,*args):
        func = func()
        print(func.encode())

    def send_resutl(self,func,*args):
        client = self.client
        func = func(*args)
        func = pickle.dumps(func)
        judge_conn = client.recv(8192).decode()
        print(judge_conn)
        client.send(b'database')
        client.recv(8192)
        client.sendall(func)
        client.recv(8192)
        client.send(b'exit')
        client.close()





#
# s = SocketSend()
# #
# s.send_resutl(stor_action.create_res_auto,'res_a','100m',1)
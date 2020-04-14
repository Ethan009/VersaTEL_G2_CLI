import pickle
import linstordb
import socket
# from stor_cmds import Action as stor_action

# ip_port = ('192.168.36.61',12129)
ip_port = ('10.203.1.89',12144)

class SocketSend():
    def __init__(self):
        self.client = socket.socket()
        self.client.connect(ip_port)
        pass


    def sql_script(self,*args):
        db = linstordb.LINSTORDB()
        return db.data_base_dump()

    def print_sql(self,func,*args):
        func = func()
        print(func.encode())

    def send_result(self,func,*args):
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

    # def send_result(self,func,*args):
    #     func = func(*args)
    #     func = pickle.dumps(func)
    #     print(func)
    #     func_str = pickle.loads(func)
    #     print('socket:')
    #     print(func_str)
    #     print(type(func_str))






#
# res = 'res_test'
# size = '100m'
# node = ['vince']
# stp = ['pool_a']
#ok

# s.send_result(stor_action.add_mirror_auto,res,1) #ok
# s.send_result(stor_action.delete_resource_des,'vince','res_test') #ok
# s.send_result(stor_action.create_storagepool_lvm,'vince','pool_b','vg3')
# s.send_result(stor_action.delete_storagepool,'vince','pool_b')
# s.send_result(stor_action.add_mirror_manual,res,node,stp)
# s.send_result(stor_action.delete_node,'vince')
# s.send_result(stor_action.create_node,'vince','192.168.36.61','Combined')


#not ok
# s.send_result(stor_action.create_res_manual,res,size,node,stp) #rd shibai return
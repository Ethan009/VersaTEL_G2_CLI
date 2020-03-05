#coding:utf-8
import iSCSIDB as db
import prettytable as pt
import colorama as ca
import functools


#上色装饰器
def coloring(func):
    @functools.wraps(func)
    def wrapper(*args):
        status_true = ['UpToDate', 'Online', 'Ok','InUse']
        result = func(*args)
        for lst in result:
            if lst[-1] in status_true:
                lst[-1] = ca.Fore.GREEN + lst[-1] + ca.Style.RESET_ALL
            else:
                lst[-1] = ca.Fore.RED + lst[-1] + ca.Style.RESET_ALL
        return result
    return wrapper



class Process_data():

    def __init__(self):
        self.linstor_db = db.LINSTORDB()
        self.linstor_db.reb_tb()
        self.cur = self.linstor_db.cur

    #获取表单行数据的通用方法
    def sql_fetch_one(self,sql):
        self.cur.execute(sql)
        date_set = self.cur.fetchone()
        return date_set

    # 获取表全部数据的通用方法
    def sql_fetch_all(self,sql):
        cur = self.cur
        cur.execute(sql)
        date_set = cur.fetchall()
        return list(date_set)


    #node
    def _select_nodetb_all(self):
        select_sql = "SELECT Node,NodeType,Addresses,State FROM nodetb"
        return self.sql_fetch_all(select_sql)


    def _select_nodetb_one(self,node):
        select_sql = "SELECT Node,NodeType,Addresses,State FROM nodetb WHERE  Node = \'%s\'"%node
        return self.sql_fetch_one(select_sql)

    def _select_res_num(self,node):
        select_sql = "SELECT COUNT(Resource) FROM resourcetb WHERE  Node = \'%s\'"%node
        return self.sql_fetch_one(select_sql)

    def _select_stp_num(self,node):
        select_sql = "SELECT COUNT(Node) FROM storagepooltb WHERE Node = \'%s\'"%node
        return self.sql_fetch_one(select_sql)

    def _select_resourcetb(self,node):
        select_sql = "SELECT DISTINCT Resource,StoragePool,Allocated,DeviceName,InUse,State FROM resourcetb WHERE Node = \'%s\'"%node
        return self.sql_fetch_all(select_sql)

    #resource
    def _get_resource(self):
        res = []
        sql_res_all = "SELECT DISTINCT Resource,Allocated,DeviceName,InUse FROM resourcetb"
        res_all = self.sql_fetch_all(sql_res_all)

        sql_res_inuse = "SELECT DISTINCT Resource,Allocated,DeviceName,InUse FROM resourcetb WHERE InUse = 'InUse'"
        in_use =  self.sql_fetch_all(sql_res_inuse)

        for i in in_use:
            res.append(i[0])

        for i in res_all:
            if i[0] in res and i[3] == 'Unused':
                res_all.remove(i)
        return res_all

    def _get_mirro_way(self,res):
        select_sql = "SELECT COUNT(Resource) FROM resourcetb WHERE Resource = \'%s\'"%res
        return self.sql_fetch_one(select_sql)

    def _get_mirror_way_son(self,res):
        select_sql = "SELECT Node,StoragePool,InUse,State FROM resourcetb WHERE Resource = \'%s\'"%res
        return self.sql_fetch_all(select_sql)

    #storagepool
    # 查询storagepooltb全部信息
    def _select_storagepooltb(self):
        select_sql = '''SELECT
            StoragePool,
            Node,
            Driver,
            PoolName,
            FreeCapacity,
            TotalCapacity,
            SupportsSnapshots,
            State
            FROM storagepooltb
            '''
        return self.sql_fetch_all(select_sql)

    def _res_sum(self,node, stp):
        select_sql = "SELECT COUNT(DISTINCT Resource) FROM resourcetb WHERE Node = '{}' AND StoragePool = '{}'".format(
            node, stp)
        num = self.sql_fetch_one(select_sql)
        return num[0]

    def _res(self,stp):
        select_sql = "SELECT Resource,Allocated,DeviceName,InUse,State FROM resourcetb WHERE StoragePool = \'%s\'"%stp
        return self.sql_fetch_all(select_sql)

    def _node_num_of_storagepool(self,stp):
        select_sql = "SELECT COUNT(Node) FROM storagepooltb WHERE StoragePool = \'%s\'"%stp
        num = self.sql_fetch_one(select_sql)
        return num[0]

    def _node_name_of_storagepool(self,stp):
        select_sql = "SELECT Node FROM storagepooltb WHERE StoragePool = \'%s\'"%stp
        date_set = self.sql_fetch_all(select_sql)
        if len(date_set) == 1:
            names = date_set[0][0]
        else:
            names = [n[0] for n in date_set]
        return names



    @coloring
    def process_data_node_all(self):
        date_list = []
        for i in self._select_nodetb_all():
            node,node_type,addr,status = i
            res_num = self._select_res_num(node)[0]
            stp_num = self._select_stp_num(node)[0]
            list_one = [node,node_type,res_num,stp_num,addr,status]
            date_list.append(list_one)
        return date_list

    #置顶文字
    def process_data_node_one(self,node):
        n = self._select_nodetb_one(node)
        node, node_type, addr, status = n
        res_num = self._select_res_num(node)[0]
        stp_num = self._select_stp_num(node)[0]
        list = [node,node_type,res_num,stp_num,addr,status]
        return tuple(list)

    @coloring
    def process_data_node_specific(self,node):
        date_list = []
        for n in self._select_resourcetb(node):
            res_name, stp_name, size, device_name, used, status = n
            list_one = [res_name, stp_name, size, device_name, used, status]
            date_list.append(list_one)
        return date_list

    @coloring
    def process_data_resource_all(self):
        date_list = []
        list_one = []
        for i in self._get_resource():
            # if i[1]: 过滤size为空的resource
            resource, size, device_name, used = i
            mirror_way = self._get_mirro_way(str(i[0]))[0]
            list_one = [resource,mirror_way,size,device_name,used]
            date_list.append(list_one)
        return date_list

    #置顶文字
    def process_data_resource_one(self,resource):
        list_one = []
        for i in self._get_resource():
            if i[0] == resource:
                if i[1]:
                    resource, size, device_name, used = i
                    mirror_way = self._get_mirro_way(str(i[0]))[0]
                    list_one = [resource, mirror_way, size, device_name, used]
        return tuple(list_one)

    @coloring
    def process_data_resource_specific(self,resource):
        data_list = []
        for res_one in self._get_mirror_way_son(resource):
            node_name, stp_name, drbd_role, status = list(res_one)
            if drbd_role == u'InUse':
                drbd_role = u'primary'
            elif drbd_role == u'Unused':
                drbd_role = u'secondary'
            list_one = [node_name,stp_name,drbd_role,status]
            data_list.append(list_one)
        return data_list

    @coloring
    def process_data_stp_all(self):
        date_list = []
        for i in self._select_storagepooltb():
            stp_name, node_name, driver, pool_name, free_size, total_size, snapshots, status = i
            res_num = self._res_sum(str(node_name), str(stp_name))
            list_one = [stp_name,node_name,res_num,driver,pool_name,free_size,total_size,snapshots,status]
            date_list.append(list_one)
        return date_list

    @coloring
    def process_data_stp_all_of_node(self,node):
        date_list = []
        for i in self._select_storagepooltb():
            stp_name, node_name, driver, pool_name, free_size, total_size, snapshots, status = i
            res_num = self._res_sum(str(node_name), str(stp_name))
            if node_name == node:
                list_one = [stp_name,node_name,res_num,driver,pool_name,free_size,total_size,snapshots,status]
                date_list.append(list_one)
        return date_list



    @coloring
    def process_data_stp_specific(self,stp):
        date_list = []
        for res in self._res(stp):
            res_name, size, device_name, used, status = res
            list_one = [res_name,size,device_name,used,status]
            date_list.append(list_one)
        return date_list



class Table_show():
    table = pt.PrettyTable()

    def __init__(self):
        ca.init(autoreset=True)

    def run(self):
        self.pd = Process_data()

    def node_all(self):
        node_all_tb = pt.PrettyTable()
        self.table.field_names = ["node", "node type", "res num", "stp num", "addr", "status"]
        for i in self.pd.process_data_node_all():
            self.table.add_row(i)
        print(self.table)

    def node_one(self,node):
        node_one_tb = pt.PrettyTable()
        node_one_tb.field_names = ['res_name','stp_name','size','device_name','used','status']
        for i in self.pd.process_data_node_specific(node):
            node_one_tb.add_row(i)

        stp_all_tb = pt.PrettyTable()
        stp_all_tb.field_names = ['stp_name','node_name','res_num','driver','pool_name','free_size','total_size','snapshots','status']
        for i in self.pd.process_data_stp_all_of_node(node):
            stp_all_tb.add_row(i)

        try:
            print("node:%s\nnodetype:%s\nresource num:%s\nstoragepool num:%s\naddr:%s\nstatus:%s"%self.pd.process_data_node_one(node))
            print(node_one_tb)
            print(stp_all_tb)
        except TypeError:
            print('Node %s does not exist.'%node)



    def resource_all(self):
        resource_all_tb = pt.PrettyTable()
        resource_all_tb.field_names = ["resource","mirror_way","size","device_name","used"]
        for i in self.pd.process_data_resource_all():
            resource_all_tb.add_row(i)
        print(resource_all_tb)

    def resource_one(self,resource):
        resource_one_tb = pt.PrettyTable()
        resource_one_tb.field_names = ['node_name','stp_name','drbd_role','status']
        for i in self.pd.process_data_resource_specific(resource):
            resource_one_tb.add_row(i)
        try:
            print("resource:%s\nmirror_way:%s\nsize:%s\ndevice_name:%s\nused:%s"%self.pd.process_data_resource_one(resource))
            print(resource_one_tb)
        except TypeError:
            print ('Resource %s does not exist.' % resource)

    def storagepool_all(self):
        stp_all_tb = pt.PrettyTable()
        stp_all_tb.field_names = ['stp_name','node_name','res_num','driver','pool_name','free_size','total_size','snapshots','status']
        for i in self.pd.process_data_stp_all():
            stp_all_tb.add_row(i)
        print(stp_all_tb)

    def storagepool_one(self,stp):
        stp_specific = pt.PrettyTable()
        stp_specific.field_names = ['res_name','size','device_name','used','status']
        for i in self.pd.process_data_stp_specific(stp):
            stp_specific.add_row(i)
        node_num = self.pd._node_num_of_storagepool(stp)
        node_name = self.pd._node_name_of_storagepool(stp)
        if node_num == 0:
            print('The storagepool does not exist')
        elif node_num == 1:
            print('Only one node (%s) exists in the storage pool named %s'%(node_name,stp))
            print(stp_specific)
        else:
            node_name = ' and '.join(node_name)
            print('The storagepool name for %s nodes is %s,they are %s.'%(node_num,stp,node_name))
            print(stp_specific)


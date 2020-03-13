#coding:utf-8
import sqlite3
import getlinstor as gi
import colorama as ca
import functools
import subprocess


class LINSTORDB():
    #LINSTOR表
    crt_sptb_sql = '''
    create table if not exists storagepooltb(
        id integer primary key, 
        StoragePool varchar(20),
        Node varchar(20),
        Driver varchar(20),
        PoolName varchar(20),
        FreeCapacity varchar(20),
        TotalCapacity varchar(20),
        SupportsSnapshots varchar(20),
        State varchar(20)
        );'''

    crt_rtb_sql = '''
    create table if not exists resourcetb(
        id integer primary key,
        Node varchar(20),
        Resource varchar(20),
        Storagepool varchar(20),
        VolumeNr varchar(20),
        MinorNr varchar(20),
        DeviceName varchar(20),
        Allocated varchar(20),
        InUse varchar(20),
        State varchar(20)
        );'''

    crt_ntb_sql = '''
    create table if not exists nodetb(
        id integer primary key,
        Node varchar(20),
        NodeType varchar(20),
        Addresses varchar(20),
        State varchar(20)
        );'''


    replace_stb_sql = '''
    replace into storagepooltb
    (
        id,
        StoragePool,
        Node,
        Driver,
        PoolName,
        FreeCapacity,
        TotalCapacity,
        SupportsSnapshots,
        State
        )
    values(?,?,?,?,?,?,?,?,?)
    '''

    replace_rtb_sql = '''
        replace into resourcetb
        (   
            id,
            Node,
            Resource,
            StoragePool,
            VolumeNr,
            MinorNr,
            DeviceName,
            Allocated,
            InUse,
            State
            )
        values(?,?,?,?,?,?,?,?,?,?)
    '''

    replace_ntb_sql = '''
        replace into nodetb
        (
            id,
            Node,
            NodeType,
            Addresses,
            State
            )
        values(?,?,?,?,?)
    '''
    #连接数据库,创建光标对象
    def __init__(self):
        #linstor.db
        self.con = sqlite3.connect(":memory:", check_same_thread=False)
        self.cur = self.con.cursor()

    #执行获取数据，删除表，创建表，插入数据
    def rebuild_tb(self):
        self.get_output()
        # self.drop_tb()
        self.create_tb()
        self.run_insert()

    def get_output(self):
        output_sp = subprocess.getoutput('linstor --no-color --no-utf8 sp l')
        output_res = subprocess.getoutput('linstor --no-color --no-utf8 r lv')
        output_node = subprocess.getoutput('linstor --no-color --no-utf8 n l')

        self.list_node = gi.GetLinstor(output_node)
        self.list_resource = gi.GetLinstor(output_res)
        self.list_storagepool = gi.GetLinstor(output_sp)


    #创建表
    def create_tb(self):
        self.cur.execute(self.crt_sptb_sql)#检查是否存在表，如不存在，则新创建表
        self.cur.execute(self.crt_rtb_sql)
        self.cur.execute(self.crt_ntb_sql)
        self.con.commit()

    #删除表，现不使用
    def drop_tb(self):
        drp_storagepooltb_sql = "drop table if exists storagepooltb"#sql语句
        drp_resourcetb_sql = "drop table if exists resourcetb"
        drp_nodetb_sql = "drop table if exists nodetb"
        self.cur.execute(drp_storagepooltb_sql)#检查是否存在表，如存在，则删除
        self.cur.execute(drp_resourcetb_sql)
        self.cur.execute(drp_nodetb_sql)
        self.con.commit()




    def rep_storagepooltb(self):
        list_data = self.list_storagepool.get_data()
        list_id = range(len(list_data))

        for i, data in zip(list_id, list_data):
            id = i
            stp, node, dri, pooln, freecap, totalcap, Snap, state = data
            self.cur.execute(self.replace_stb_sql, (id, stp, node, dri, pooln, freecap, totalcap, Snap, state))

    def rep_resourcetb(self):
        list_data = self.list_resource.get_data()
        list_id = range(len(list_data))
        for i, data in zip(list_id,list_data):
            id = i
            node, res, stp, voln, minorn, devname, allocated, use, state = data
            self.cur.execute(self.replace_rtb_sql, (id, node, res, stp, voln, minorn, devname, allocated, use, state))

    def rep_nodetb(self):
        list_data = self.list_node.get_data()
        list_id = range(len(list_data))
        for i, data in zip(list_id,list_data):
            id = i
            node, nodetype, addr, state = data
            self.cur.execute(self.replace_ntb_sql, (id, node, nodetype, addr, state))


    def run_insert(self):
        self.rep_storagepooltb()
        self.rep_resourcetb()
        self.rep_nodetb()
        self.con.commit()


    def data_base_dump(self):
        cur = self.cur
        con = self.con
        self.rebuild_tb()
        SQL_script = con.iterdump()
        cur.close()
        return "\n".join(SQL_script)




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



class DataProcess():
    def __init__(self):
        self.linstor_db = LINSTORDB()
        self.linstor_db.rebuild_tb()
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
        self.cur.close()
        return date_list

    #置顶文字
    def process_data_node_one(self,node):
        n = self._select_nodetb_one(node)
        node, node_type, addr, status = n
        res_num = self._select_res_num(node)[0]
        stp_num = self._select_stp_num(node)[0]
        list = [node,node_type,res_num,stp_num,addr,status]
        self.cur.close()
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
            if i[1]: #过滤size为空的resource
                resource, size, device_name, used = i
                mirror_way = self._get_mirro_way(str(i[0]))[0]
                list_one = [resource,mirror_way,size,device_name,used]
                date_list.append(list_one)
        self.cur.close()
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
        self.cur.close()
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
        self.cur.close()
        return data_list

    @coloring
    def process_data_stp_all(self):
        date_list = []
        for i in self._select_storagepooltb():
            stp_name, node_name, driver, pool_name, free_size, total_size, snapshots, status = i
            res_num = self._res_sum(str(node_name), str(stp_name))
            list_one = [stp_name,node_name,res_num,driver,pool_name,free_size,total_size,snapshots,status]
            date_list.append(list_one)
        self.cur.close()
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
        self.cur.close()
        return date_list



    @coloring
    def process_data_stp_specific(self,stp):
        date_list = []
        for res in self._res(stp):
            res_name, size, device_name, used, status = res
            list_one = [res_name,size,device_name,used,status]
            date_list.append(list_one)
        self.cur.close()
        return date_list


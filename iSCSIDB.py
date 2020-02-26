#coding:utf-8
import sqlite3
import GetLinstor as gi #修改
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
    #连接数据库
    def __init__(self):
        self.con = sqlite3.connect("iscsi.db",check_same_thread=False)
        self.cur = self.con.cursor()

    def rebuild_tb(self):
        self.get_op()
        self.drop_tb()
        self.create_tb()
        self.run_rep()

    def get_op(self):
        output_storagepool = subprocess.getoutput('linstor sp l')
        output_resource = subprocess.getoutput('linstor r lv')
        output_node = subprocess.getoutput('linstor n l')
        self.info_storagepool = gi.GetLinstor(output_storagepool)
        self.info_resource = gi.GetLinstor(output_resource)
        self.info_node = gi.GetLinstor(output_node)

    #创建表
    def create_tb(self):
        self.cur.execute(self.crt_sptb_sql)#检查是否存在表，如不存在，则新创建表
        self.cur.execute(self.crt_rtb_sql)
        self.cur.execute(self.crt_ntb_sql)
        self.con.commit()

    #delete table
    def drop_tb(self):
        drp_storagepooltb_sql = "drop table if exists storagepooltb"#sql语句
        drp_resourcetb_sql = "drop table if exists resourcetb"
        drp_nodetb_sql = "drop table if exists nodetb"
        self.cur.execute(drp_storagepooltb_sql)#检查是否存在表，如存在，则删除
        self.cur.execute(drp_resourcetb_sql)
        self.cur.execute(drp_nodetb_sql)
        self.con.commit()

    #adding data to the table
    def rep_storagepooltb(self):
        for n, i in zip(range(len(self.info_storagepool.list_result))[1:], self.info_storagepool.list_result[1:]):
            id = n
            stp, node, dri, pooln, freecap, totalcap, Snap, state = i
            self.cur.execute(self.replace_stb_sql, (id, stp, node, dri, pooln, freecap, totalcap, Snap, state))

    def rep_resourcetb(self):
        for n, i in zip(range(len(self.info_resource.list_result))[1:], self.info_resource.list_result[1:]):
            id = n
            node, res, stp, voln, minorn, devname, allocated, use, state = i
            self.cur.execute(self.replace_rtb_sql, (id, node, res, stp, voln, minorn, devname, allocated, use, state))

    def rep_nodetb(self):
        for n, i in zip(range(len(self.info_node.list_result))[1:], self.info_node.list_result[1:]):
            id = n
            node, nodetype, addr, state = i
            self.cur.execute(self.replace_ntb_sql, (id, node, nodetype, addr, state))

    def get_lun_name(self,device_name):
        select_sql = "select Resource from resource where DeviceName = '"+device_name+"'"
        self.cur.execute(select_sql)
        date_set = self.cur.fetchone()
        return list(date_set)


    def run_rep(self):
        self.rep_storagepooltb()
        self.rep_resourcetb()
        self.rep_nodetb()
        self.con.commit()


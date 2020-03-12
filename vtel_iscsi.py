#coding=utf-8
import argparse
import json
import os
from pprint import pprint
from crm_resouce import crmdata
"""
@author: Zane
@note: VersaTEL-iSCSI
@time: 2020/02/18
"""

class CLI():
	def __init__(self):
		self.parser_vtel()
		self.parser_stor()
		self.parser_iscsi()
		self.args = self.vtel.parse_args()
		self.iscsi_judge()


	def parser_vtel(self):
		self.vtel = argparse.ArgumentParser(prog='vtel',formatter_class=argparse.RawTextHelpFormatter, add_help=False)
		sub_vtel = self.vtel.add_subparsers(dest='vtel_sub')

		# add all sub parse
		self.vtel_stor = sub_vtel.add_parser('stor',help='Management operations for LINSTOR',add_help=False)
		self.vtel_iscsi = sub_vtel.add_parser('iscsi',help='Management operations for iSCSI',add_help=False)
		self.vtel_fc = sub_vtel.add_parser('fc',help='for fc resource management...',add_help=False)
		self.vtel_ceph = sub_vtel.add_parser('ceph',help='for ceph resource management...',add_help=False)


	def parser_stor(self):
		##stor
		sub_stor = self.vtel_stor.add_subparsers(dest='stor_sub')
		self.stor_node = sub_stor.add_parser('node', aliases='n', help='Management operations for node')
		self.stor_resource = sub_stor.add_parser('resource', aliases='r', help='Management operations for storagepool')
		self.stor_storagepool = sub_stor.add_parser('storagepool', aliases=['sp'],help='Management operations for storagepool')
		self.stor_snap = sub_stor.add_parser('snap', aliases=['sn'], help='Management operations for snapshot')


	def parser_iscsi(self):
		## iscsi
		sub_iscsi = self.vtel_iscsi.add_subparsers(dest='iscsi')
		self.iscsi_host = sub_iscsi.add_parser('host',help='host operation', add_help=False)
		self.iscsi_hostgroup = sub_iscsi.add_parser('hg',help='hostgroup operation', add_help=False)
		self.iscsi_diskgroup = sub_iscsi.add_parser('dg',help='diskgroup operation', add_help=False)
		self.iscsi_map = sub_iscsi.add_parser('map',help='map operation', add_help=False)

		### iscsi host
		sub_iscsi_host = self.iscsi_host.add_subparsers(dest='host')
		self.iscsi_host_create = sub_iscsi_host.add_parser('create',help='host create')
		self.iscsi_host_show = sub_iscsi_host.add_parser('show',help='host show')
		self.iscsi_host_delete = sub_iscsi_host.add_parser('delete',help='host delete')
		#self.iscsi_host_modify = sub_iscsi_host.add_parser('modify',help='host modify')

		### iscsi hostgroup
		sub_iscsi_hostgroup = self.iscsi_hostgroup.add_subparsers(dest='hostgroup')
		self.iscsi_hostgroup_create = sub_iscsi_hostgroup.add_parser('create',help='hostgroup create')
		self.iscsi_hostgroup_show = sub_iscsi_hostgroup.add_parser('show',help='hostgroup show')
		self.iscsi_hostgroup_delete = sub_iscsi_hostgroup.add_parser('delete',help='hostgroup delete')

		### iscsi diskgroup
		sub_iscsi_diskgroup = self.iscsi_diskgroup.add_subparsers(dest='diskgroup')
		self.iscsi_diskgroup_create = sub_iscsi_diskgroup.add_parser('create',help='diskgroup create')
		self.iscsi_diskgroup_show = sub_iscsi_diskgroup.add_parser('show',help='diskgroup show')
		self.iscsi_diskgroup_delete = sub_iscsi_diskgroup.add_parser('delete',help='diskgroup delete')

		### iscsi map
		sub_iscsi_map = self.iscsi_map.add_subparsers(dest='map')
		self.iscsi_map_create = sub_iscsi_map.add_parser('create',help='map create')
		self.iscsi_map_show = sub_iscsi_map.add_parser('show',help='map show')
		self.iscsi_map_delete = sub_iscsi_map.add_parser('delete',help='map delete')

		#### iscsi host argument
		self.iscsi_host_create.add_argument('iqnname',action='store',help='hostname')
		self.iscsi_host_create.add_argument('iqn',action='store',help='iqn')
		self.iscsi_host_show.add_argument('show',action='store',help='host show',nargs='?',default='all')	
		self.iscsi_host_delete.add_argument('iqnname',action='store',help='iqnname',default=None)

		#### iscsi hostgroup argument
		self.iscsi_hostgroup_create.add_argument('hostgroupname',action='store',help='hostgroup_create name')
		self.iscsi_hostgroup_create.add_argument('iqnname',action='store',help='hostgroup_create hostname',nargs='+')
		self.iscsi_hostgroup_show.add_argument('show',action='store',help='hostgroup_show',nargs='?',default='all')
		self.iscsi_hostgroup_delete.add_argument('hostgroupname',action='store',help='hostgroup_delete name',default=None)

		#### iscsi diskgroup argument
		self.iscsi_diskgroup_create.add_argument('diskgroupname',action='store',help='diskgroup_create name')
		self.iscsi_diskgroup_create.add_argument('diskname',action='store',help='diskgroup_create diskname',nargs='+')
		self.iscsi_diskgroup_show.add_argument('show',action='store',help='diskgroup_show',nargs='?',default='all')
		self.iscsi_diskgroup_delete.add_argument('diskgroupname',action='store',help='diskgroup_delete',default=None)

		#### iscsi map argument
		self.iscsi_map_create.add_argument('mapname',action='store',help='map name')
		self.iscsi_map_create.add_argument('-hg',action='store',help='hostgroupname')
		self.iscsi_map_create.add_argument('-dg',action='store',help='diskgroupname')
		self.iscsi_map_show.add_argument('show',action='store',help='diskgroup_show',nargs='?',default='all')
		self.iscsi_map_delete.add_argument('mapname',action='store',help='diskgroup_delete',default=None)

	# 命令判断
	def iscsi_judge(self):
		js = JSON_OPERATION()
		args = self.args
		if args.iscsi == 'host':
			if args.host == 'create':
				self.judge_hc(args, js)
			elif args.host == 'show':
				self.judge_hs(args, js)
			elif args.host == 'delete':
				self.judge_hd(args, js)
			else:
				print("iscsi host ? (choose from 'create', 'show', 'delete')")
		elif args.iscsi == 'hg':
			if args.hostgroup == 'create':
				self.judge_hgc(args, js)
			elif args.hostgroup == 'show':
				self.judge_hgs(args, js)
			elif args.hostgroup == 'delete':
				self.judge_hgd(args, js)
			else:
				print("iscsi hostgroup ? (choose from 'create', 'show', 'delete')")
		elif args.iscsi == 'dg':
			if args.diskgroup == 'create':
				self.judge_dgc(args, js)
			elif args.diskgroup == 'show':
				self.judge_dgs(args, js)
			elif args.diskgroup == 'delete':
				self.judge_dgd(args, js)
			else:
				print("iscsi diskgroup ? (choose from 'create', 'show', 'delete')")
		elif args.iscsi == 'map':
			if args.map == 'create':
				self.judge_mc(args, js)
			elif args.map == 'show':
				self.judge_ms(args, js)
			elif args.map == 'delete':
				self.judge_md(args, js)
			else:
				print("iscsi map ? (choose from 'create', 'show', 'delete')")
		else:
			print("iscsi ？ (choose from 'host', 'hg', 'dg', 'map')")

	# host创建
	def judge_hc(self, args, js):
		print("hostname:",args.iqnname)
		print("host:",args.iqn)
		if js.check_key('Host',args.iqnname):
			print("Fail! The Host " + args.iqnname + " already existed.")
		else:
			js.creat_data("Host",args.iqnname,args.iqn)
			print("Create success!")

	# host查询
	def judge_hs(self, args, js):
		if args.show == 'all' or args.show == None:
			print("Host:")
			hosts = js.get_data("Host")
			for k in hosts:
				print("	" + k + ": " + hosts[k])
		else:
			if js.check_key('Host',args.show):
				print(args.show, ":", js.get_data('Host').get(args.show))
			else:
				print("Fail! Can't find " + args.show)

	# host删除
	def judge_hd(self, args, js):
		print("Delete the host witch name is",args.iqnname,"...")
		if js.check_key('Host',args.iqnname):
			if js.check_value('HostGroup',args.iqnname):
				print("Fail! The host in sameone hostgroup,Please delete the hostgroup first")
			else:
				js.delete_data('Host',args.iqnname)
				print("Delete success!")
		else:
			print("Fail! Can't find " + args.iqnname)

	# hostgroup创建
	def judge_hgc(self, args, js):
		print("hostgroupname:",args.hostgroupname)
		print("iqn name:",args.iqnname)
		if js.check_key('HostGroup',args.hostgroupname):
			print("Fail! The HostGroup " + args.hostgroupname + " already existed.")
		else:
			t = True
			for i in args.iqnname:
				if js.check_key('Host',i) == False:
					t = False
					print("Fail! Can't find " + i)
			if t:
				js.creat_data('HostGroup',args.hostgroupname,args.iqnname)
				print("Create success!")
			else:
				print("Fail! Please give the true name.")

	# hostgroup查询
	def judge_hgs(self, args, js):
		if args.show == 'all' or args.show == None:
			print("Hostgroup:")
			hostgroups = js.get_data("HostGroup")
			for k in hostgroups:
				print("	" + k + ":")
				for v in hostgroups[k]:
					print("		" + v)
		else:
			if js.check_key('HostGroup',args.show):
				print(args.show + ":")
				for k in js.get_data('HostGroup').get(args.show):
					print("	" + k)
			else:
				print("Fail! Can't find " + args.show)

	# hostgroup删除
	def judge_hgd(self, args, js):
		print("Delete the hostgroup witch name is",args.hostgroupname)
		if js.check_key('HostGroup',args.hostgroupname):
			if js.check_value('Map',args.hostgroupname):
				print("Fail! The hostgroup already map,Please delete the map")
			else:
				js.delete_data('HostGroup',args.hostgroupname)
				print("Delete success!")
		else:
			print("Fail! Can't find " + args.hostgroupname)

	# diskgroup创建
	def judge_dgc(self, args, js):
		print("diskgroupname:",args.diskgroupname)
		print("disk name:",args.diskname)
		if js.check_key('DiskGroup',args.diskgroupname):
			print("Fail! The DiskGroup " + args.diskgroupname + " already existed.")
		else:
			t = True
			for i in args.diskname:
				if js.check_key('Disk',i) == False:
					t = False
					print("Fail! Can't find " + i)
			if t:
				js.creat_data('DiskGroup',args.diskgroupname,args.diskname)
				print("Create success!")
			else:
				print("Fail! Please give the true name.")

	# diskgroup查询
	def judge_dgs(self, args, js):
		if args.show == 'all' or args.show == None:
			print("Diskgroup:")
			diskgroups = js.get_data("DiskGroup")
			for k in diskgroups:
				print("	" + k + ":")
				for v in diskgroups[k]:
					print("		" + v)
		else:
			if js.check_key('DiskGroup',args.show):
				print(args.show + ":")
				for k in js.get_data('DiskGroup').get(args.show):
					print("	" + k)
			else:
				print("Fail! Can't find " + args.show)

	# diskgroup删除
	def judge_dgd(self, args, js):
		print("Delete the diskgroup witch name is",args.diskgroupname,"...")
		if js.check_key('DiskGroup',args.diskgroupname):
			if js.check_value('Map',args.diskgroupname):
				print("Fail! The diskgroup already map,Please delete the map")
			else:
				js.delete_data('DiskGroup',args.diskgroupname)
				print("Delete success!")
		else:
			print("Fail! Can't find " + args.diskgroupname)

	# map创建
	def judge_mc(self, args, js):
		print("map name:",args.mapname)
		print("hostgroup name:",args.hg)
		print("diskgroup name:",args.dg)
		self.crm_up(js)
		if js.check_key('Map',args.mapname):
			print("The Map \"" + args.mapname + "\" already existed.")
		elif js.check_key('HostGroup',args.hg) == False:
			print("Can't find "+args.hg)
		elif js.check_key('DiskGroup',args.dg) == False:
			print("Can't find "+args.dg) 
		else:
			if js.check_value('Map',args.dg) == True:
				print("The diskgroup already map")
			js.creat_data('Map',args.mapname,[args.hg,args.dg])
			print("Create success!")

	# map查询
	def judge_ms(self, args, js):
		self.crm_up(js)
		if args.show == 'all' or args.show == None:
			print("Map:")
			maps = js.get_data("Map")
			for k in maps:
				print("	" + k + ":")
				for v in maps[k]:
					print("		" + v)
		else:
			if js.check_key('Map',args.show):
				print(args.show + ":")
				for k in js.get_data('Map').get(args.show):
					print("	" + k)
			else:
				print("Fail! Can't find " + args.show)

	# map删除
	def judge_md(self, args, js):
		print("Delete the map witch name is",args.mapname,"...")
		if js.check_key('Map',args.mapname):
			print(js.get_data('Map').get(args.mapname),"will probably be affected ")
			js.delete_data('Map',args.mapname)
			print("Delete success!")
		else:
			print("Fail! Can't find " + args.mapname)

	# 获取并更新crm信息
	def crm_up(self, js):
		cd = crmdata()
		crm_config_statu = cd.re_data()
		print("update crm_config_statu :")
		print("	", crm_config_statu, "\n")
		js.up_crmconfig(crm_config_statu)


class JSON_OPERATION:

    def __init__(self):
        self.read_data = self.read_data_json()

    def read_data_json(self):
        rdata = open("iSCSI_Data.json", encoding='utf-8')
        read_json_dict = json.load(rdata)
        rdata.close
        return read_json_dict

    #创建Host、Disk、Target、HostGroup、DiskGroup,Map
    def creat_data(self,first_key,data_key,data_value):
        self.read_data[first_key].update({data_key:data_value})
        with open('iSCSI_Data.json', "w") as fw:
            json.dump(self.read_data, fw)

    #删除Host、Disk、Target，HostGroup、DiskGroup,Map
    def delete_data(self,first_key,data_key):
        self.read_data[first_key].pop(data_key)
        with open('iSCSI_Data.json', "w") as fw:
            json.dump(self.read_data, fw)

    #获取Host,Disk、Target，HostGroup、DiskGroup,Map的信息
    def get_data(self, first_key):
        all_data = self.read_data[first_key]
        return all_data

    #检查key值是否存在
    def check_key(self, first_key, data_key):
    	if data_key in self.read_data[first_key]:
    		return True
    	else:
    		return False

	#检查value值是否存在
    def check_value(self, first_key, data_value):
    	for key in self.read_data[first_key]:
    		if data_value in self.read_data[first_key][key]:
    			return True
    	return False

	#更新crm configure资源的信息
    def up_crmconfig(self, data):
    	self.read_data.update({'crm':{}})
    	self.read_data['crm'].update({'resource':data[0]})
    	self.read_data['crm'].update({'vip':data[1]})
    	self.read_data['crm'].update({'target':data[2]})
    	with open('iSCSI_Data.json', "w") as fw:
    		json.dump(self.read_data, fw)


if __name__ == '__main__':
	args = CLI()
	# print(args.args)
	

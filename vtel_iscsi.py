#coding=utf-8
import argparse
import json
import os
from pprint import pprint
from crm_resouce import crm
from getlinstor import GetLinstor
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
		self.vtel_iscsi = sub_vtel.add_parser('iscsi',help='Management operations for iSCSI')
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
		self.iscsi_host = sub_iscsi.add_parser('host',aliases='h', help='host operation')
		self.iscsi_disk = sub_iscsi.add_parser('disk',aliases='d', help='disk operation')
		self.iscsi_hostgroup = sub_iscsi.add_parser('hostgroup',aliases=['hg'],help='hostgroup operation')
		self.iscsi_diskgroup = sub_iscsi.add_parser('diskgroup',aliases=['dg'],help='diskgroup operation')
		self.iscsi_map = sub_iscsi.add_parser('map',aliases='m',help='map operation')
		# self.iscsi_gui = sub_iscsi.add_parser('gui',help='iscsi gui')
		# self.iscsi_gui.add_argument('i',help='gui data')


		### iscsi host
		sub_iscsi_host = self.iscsi_host.add_subparsers(dest='host')
		self.iscsi_host_create = sub_iscsi_host.add_parser('create', aliases='c', help='host create [host_name] [host_iqn]')
		self.iscsi_host_show = sub_iscsi_host.add_parser('show', aliases='s', help='host show / host show [host_name]')
		self.iscsi_host_delete = sub_iscsi_host.add_parser('delete', aliases='d', help='host delete [host_name]')
		#self.iscsi_host_modify = sub_iscsi_host.add_parser('modify',help='host modify')

		### iscsi disk
		sub_iscsi_disk = self.iscsi_disk.add_subparsers(dest='disk')
		self.iscsi_disk_show = sub_iscsi_disk.add_parser('show', aliases='s', help='disk show')

		### iscsi hostgroup
		sub_iscsi_hostgroup = self.iscsi_hostgroup.add_subparsers(dest='hostgroup')
		self.iscsi_hostgroup_create = sub_iscsi_hostgroup.add_parser('create', aliases='c', help='hostgroup create [hostgroup_name] [host_name1] [host_name2] ...')
		self.iscsi_hostgroup_show = sub_iscsi_hostgroup.add_parser('show', aliases='s', help='hostgroup show / hostgroup show [hostgroup_name]')
		self.iscsi_hostgroup_delete = sub_iscsi_hostgroup.add_parser('delete', aliases='d', help='hostgroup delete [hostgroup_name]')

		### iscsi diskgroup
		sub_iscsi_diskgroup = self.iscsi_diskgroup.add_subparsers(dest='diskgroup')
		self.iscsi_diskgroup_create = sub_iscsi_diskgroup.add_parser('create', aliases='c', help='diskgroup create [diskgroup_name] [disk_name1] [disk_name2] ...')
		self.iscsi_diskgroup_show = sub_iscsi_diskgroup.add_parser('show', aliases='s', help='diskgroup show / diskgroup show [diskgroup_name]')
		self.iscsi_diskgroup_delete = sub_iscsi_diskgroup.add_parser('delete', aliases='d', help='diskgroup delete [diskgroup_name]')

		### iscsi map
		sub_iscsi_map = self.iscsi_map.add_subparsers(dest='map')
		self.iscsi_map_create = sub_iscsi_map.add_parser('create', aliases='c', help='map create [map_name] -hg [hostgroup_name] -dg [diskgroup_name]')
		self.iscsi_map_show = sub_iscsi_map.add_parser('show', aliases='s', help='map show / map show [map_name]')
		self.iscsi_map_delete = sub_iscsi_map.add_parser('delete', aliases='d', help='map delete [map_name]')

		#### iscsi host argument
		self.iscsi_host_create.add_argument('iqnname',action='store',help='host_name')
		self.iscsi_host_create.add_argument('iqn',action='store',help='host_iqn')
		self.iscsi_host_show.add_argument('show',action='store',help='host show [host_name]',nargs='?',default='all')	
		self.iscsi_host_delete.add_argument('iqnname',action='store',help='host_name',default=None)

		#### iscsi disk argument
		self.iscsi_disk_show.add_argument('show',action='store',help='disk show [disk_name]',nargs='?',default='all')

		#### iscsi hostgroup argument
		self.iscsi_hostgroup_create.add_argument('hostgroupname',action='store',help='hostgroup_name')
		self.iscsi_hostgroup_create.add_argument('iqnname',action='store',help='host_name',nargs='+')
		self.iscsi_hostgroup_show.add_argument('show',action='store',help='hostgroup show [hostgroup_name]',nargs='?',default='all')
		self.iscsi_hostgroup_delete.add_argument('hostgroupname',action='store',help='hostgroup_name',default=None)

		#### iscsi diskgroup argument
		self.iscsi_diskgroup_create.add_argument('diskgroupname',action='store',help='diskgroup_name')
		self.iscsi_diskgroup_create.add_argument('diskname',action='store',help='disk_name',nargs='+')
		self.iscsi_diskgroup_show.add_argument('show',action='store',help='diskgroup show [diskgroup_name]',nargs='?',default='all')
		self.iscsi_diskgroup_delete.add_argument('diskgroupname',action='store',help='diskgroup_name',default=None)

		#### iscsi map argument
		self.iscsi_map_create.add_argument('mapname',action='store',help='map_name')
		self.iscsi_map_create.add_argument('-hg',action='store',help='hostgroup_name')
		self.iscsi_map_create.add_argument('-dg',action='store',help='diskgroup_name')
		self.iscsi_map_show.add_argument('show',action='store',help='map show [map_name]',nargs='?',default='all')
		self.iscsi_map_delete.add_argument('mapname',action='store',help='map_name',default=None)

	# 命令判断
	def iscsi_judge(self):
		js = JSON_OPERATION()
		args = self.args
		if args.iscsi in ['host', 'h']:
			if args.host in ['create', 'c']:
				self.judge_hc(args, js)
			elif args.host in ['show', 's']:
				self.judge_hs(args, js)
			elif args.host in ['delete', 'd']:
				self.judge_hd(args, js)
			else:
				print("iscsi host ? (choose from 'create', 'show', 'delete')")
		elif args.iscsi in ['disk','d']:
			if args.disk in ['show','s']:
				self.judge_ds(args, js)
			else:
				print("iscsi disk ? (choose from 'show')")
		elif args.iscsi in ['hostgroup','hg']:
			if args.hostgroup in ['create', 'c']:
				self.judge_hgc(args, js)
			elif args.hostgroup in ['show', 's']:
				self.judge_hgs(args, js)
			elif args.hostgroup in ['delete', 'd']:
				self.judge_hgd(args, js)
			else:
				print("iscsi hostgroup ? (choose from 'create', 'show', 'delete')")
		elif args.iscsi in ['diskgroup','dg']:
			if args.diskgroup in ['create', 'c']:
				self.judge_dgc(args, js)
			elif args.diskgroup in ['show', 's']:
				self.judge_dgs(args, js)
			elif args.diskgroup in ['delete', 'd']:
				self.judge_dgd(args, js)
			else:
				print("iscsi diskgroup ? (choose from 'create', 'show', 'delete')")
		elif args.iscsi in ['map','m']:
			if args.map in ['create', 'c']:
				self.judge_mc(args, js)
			elif args.map in ['show', 's']:
				self.judge_ms(args, js)
			elif args.map in ['delete', 'd']:
				self.judge_md(args, js)
			else:
				print("iscsi map ? (choose from 'create', 'show', 'delete')")
		elif args.iscsi == 'gui':
			print(args.gui)
		else:
			print("iscsi ？ (choose from 'host', 'disk', 'hg', 'dg', 'map')")

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
		print(type(args))
		if args.show == 'all' or args.show == None:
			hosts = js.get_data("Host")
			print("	" + "{:<15}".format("Hostname") + "Iqn")
			print("	" + "{:<15}".format("---------------") + "---------------")
			for k in hosts:
				print("	" + "{:<15}".format(k) + hosts[k])
		else:
			if js.check_key('Host',args.show):
				print(args.show, ":", js.get_data('Host').get(args.show))
			else:
				print("Fail! Can't find " + args.show)
		return True

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

	# disk查询
	def judge_ds(self, args, js):
		cd = crm()
		# data = cd.lsdata()
		data = cd.get_data_linstor()
		linstorlv = GetLinstor(data)
		disks = {}
		for d in linstorlv.get_data():
			disks.update({d[1]:d[5]})
		js.up_data('Disk',disks)
		if args.show == 'all' or args.show == None:
			print("	" + "{:<15}".format("Diskname") + "Path")
			print("	" + "{:<15}".format("---------------") + "---------------")
			for k in disks:
				print("	" + "{:<15}".format(k) + disks[k])
		else:
			if js.check_key('Disk',args.show):
				print(args.show, ":", js.get_data('Disk').get(args.show))
			else:
				print("Fail! Can't find " + args.show)


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
				print("	" + "---------------")
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
				print("	" + "---------------")
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
		crmdata = self.crm_up(js)
		if js.check_key('Map',args.mapname):
			print("The Map \"" + args.mapname + "\" already existed.")
		elif js.check_key('HostGroup',args.hg) == False:
			print("Can't find "+args.hg)
		elif js.check_key('DiskGroup',args.dg) == False:
			print("Can't find "+args.dg) 
		else:
			if js.check_value('Map',args.dg) == True:
				print("The diskgroup already map")
			mapdata = self.map_data(js, crmdata, args.hg, args.dg)
			print(mapdata)
			self.map_crm_c(mapdata)
			js.creat_data('Map',args.mapname,[args.hg,args.dg])
			print("Create success!")

	# map查询
	def judge_ms(self, args, js):
		self.crm_up(js)
		if args.show == 'all' or args.show == None:
			print("Map:")
			maps = js.get_data("Map")
			for k in maps:
				print("	" + "---------------")
				print("	" + k + ":")
				for v in maps[k]:
					print("		" + v)
		else:
			if js.check_key('Map',args.show):
				print(args.show + ":")
				maplist = js.get_data('Map').get(args.show)
				print('	' + maplist[0] + ':')
				for i in js.get_data('HostGroup').get(maplist[0]):
					print('		' + i + ': ' + js.get_data('Host').get(i))
				print('	' + maplist[1] + ':')
				for i in js.get_data('DiskGroup').get(maplist[1]):
					print('		' + i + ': ' + js.get_data('Disk').get(i))
			else:
				print("Fail! Can't find " + args.show)

	# map删除
	def judge_md(self, args, js):
		print("Delete the map witch name is", args.mapname)
		if js.check_key('Map',args.mapname):
			print(js.get_data('Map').get(args.mapname),"will probably be affected ")
			resname = self.map_data_d(js, args.mapname)
			self.map_crm_d(resname)
			js.delete_data('Map',args.mapname)
			print("Delete success!")
		else:
			print("Fail! Can't find " + args.mapname)

	# 获取并更新crm信息
	def crm_up(self, js):
		cd = crm()
		crm_config_statu = cd.re_data()
		# pprint(crm_config_statu)
		js.up_crmconfig(crm_config_statu)
		return crm_config_statu

	# 获取创建map所需的数据
	def map_data(self, js, crmdata, hg, dg):
		mapdata = {}
		hostiqn = []
		for h in js.get_data('HostGroup').get(hg):
			iqn = js.get_data('Host').get(h)
			hostiqn.append(iqn)
		mapdata.update({'host_iqn':hostiqn})
		disk = js.get_data('DiskGroup').get(dg)
		cd = crm()
		# data = cd.lsdata()
		data = cd.get_data_linstor()
		linstorlv = GetLinstor(data)
		print("get linstor r lv data:")
		print(linstorlv)
		diskd = {}
		for d in linstorlv.get_data():
			for i in disk:
				if i in d:
					diskd.update({d[1]:[d[4],d[5]]})
		mapdata.update({'disk':diskd})
		mapdata.update({'target':crmdata[2]})
		# print(mapdata)
		return mapdata

	# 获取删除map所需的数据
	def map_data_d(self, js, mapname):
		dg = js.get_data('Map').get(mapname)[1]
		disk = js.get_data('DiskGroup').get(dg)
		return disk

	# 调用crm创建map
	def map_crm_c(self, mapdata):
		cd = crm()
		for i in mapdata['target']:
			target = i[0]
			targetiqn = i[1]
		# print(mapdata['disk'])
		for disk in mapdata['disk']:
			res = [disk, mapdata['disk'].get(disk)[0], mapdata['disk'].get(disk)[1]]
			cd.createres(res, mapdata['host_iqn'], targetiqn)
			cd.createco(res[0], target)
			cd.resstart(res[0])
			print(" ")

	# 调用crm删除map
	def map_crm_d(self, resname):
		cd = crm()
		for disk in resname:
			cd.delres(disk)
			print(" ")
		return True


class JSON_OPERATION:

    def __init__(self):
        self.read_data = self.read_data_json()

    def read_data_json(self):
        rdata = open("iSCSI_Data.json", encoding='utf-8')
        read_json_dict = json.load(rdata)
        rdata.close
        return read_json_dict

    #创建Host、HostGroup、DiskGroup,Map
    def creat_data(self,first_key,data_key,data_value):
        self.read_data[first_key].update({data_key:data_value})
        with open('iSCSI_Data.json', "w") as fw:
            json.dump(self.read_data, fw)

    #删除Host、HostGroup、DiskGroup,Map
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

    #更新disk
    def up_data(self,first_key,data):
        self.read_data[first_key] = data
        with open('iSCSI_Data.json', "w") as fw:
            json.dump(self.read_data, fw)

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

	

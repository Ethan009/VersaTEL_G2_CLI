import re
import subprocess
import time

"""
@author: Zane
@note: VersaTEL-iSCSI获取crm信息
@time: 2020/03/11
"""
class crmdata():
	"""docstring for crm_data"""
	def __init__(self):
		
		self.iscsistatu = r'''primitive apple iSCSILogicalUnit \
			params target_iqn="iqn.2019-09.feixitek.com:1" implementation=lio-t lun=5 path="/dev/drbd1000" allowed_initiators="iqn.1993-08.org.debian:01:bc429d5fc3b iqn.1991-05.com.microsoft:win7tian" \
			        meta target-role=Started
			primitive ben iSCSILogicalUnit \
			        params target_iqn="iqn.2019-09.feixitek.com:1" implementation=lio-t lun=2 path="/dev/drbd1005" allowed_initiators="iqn.1993-08.org.debian:01:1cc967493b4 iqn.1993-08.org.debian:01:181885d4e7d7" \
			        meta target-role=Started
			primitive fred iSCSILogicalUnit \
			        params target_iqn="iqn.2019-09.feixitek.com:1" implementation=lio-t lun=4 path="/dev/drbd1003" allowed_initiators="iqn.1993-08.org.debian:01:bc429d5fc3b iqn.1991-05.com.microsoft:win7tian" \
			        meta target-role=Started
			primitive iscsi_target_test iSCSITarget \
			        params iqn="iqn.2019-09.feixitek.com:1" implementation=lio-t portals="10.203.1.33:3260" \
			        op start timeout=20 interval=0 \
			        op stop timeout=20 interval=0 \
			        op monitor interval=20 timeout=40
			primitive iscsi_target_test1 iSCSITarget \
			        params iqn="iqn.2019-09.feixitek.com:2" implementation=lio-t portals="10.203.1.33:3260" \
			        op start timeout=20 interval=0 \
			        op stop timeout=20 interval=0 \
			        op monitor interval=20 timeout=40
			primitive p_drbd_linstordb ocf:linbit:drbd \
			        params drbd_resource=linstordb \
			        op monitor interval=29 role=Master \
			        op monitor interval=30 role=Slave \
			        op start interval=0 timeout=240s \
			        op stop interval=0 timeout=100s
			primitive p_fs_linstordb Filesystem \
			        params device="/dev/drbd/by-res/linstordb/0" directory="/var/lib/linstor" fstype=xfs \
			        op start interval=0 timeout=60s \
			        op stop interval=0 timeout=100s \
			        op monitor interval=20s timeout=40s
			primitive p_iscsi_portblock_off_drbd0 portblock \
			        params ip=10.203.1.33 portno=3260 protocol=tcp action=unblock \
			        op start timeout=20 interval=0 \
			        op stop timeout=20 interval=0 \
			        op monitor timeout=20 interval=20
			primitive p_iscsi_portblock_on_drbd0 portblock \
			        params ip=10.203.1.33 portno=3260 protocol=tcp action=block \
			        op start timeout=20 interval=0 \
			        op stop timeout=20 interval=0 \
			        op monitor timeout=20 interval=20
			primitive p_linstor-controller systemd:linstor-controller \
			        op start interval=0 timeout=100s \
			        op stop interval=0 timeout=100s \
			        op monitor interval=30s timeout=100s \
			        meta is-managed=true
			primitive seven iSCSILogicalUnit \
			        params target_iqn="iqn.2019-09.feixitek.com:1" implementation=lio-t lun=1 path="/dev/drbd1006" allowed_initiators="iqn.1993-08.org.debian:01:e3589b7c9ce iqn.1991-05.com.microsoft:win7mark" \
			        op monitor interval=10s \
			        meta target-role=Started
			primitive test iSCSILogicalUnit \
			        params target_iqn="iqn.2019-09.feixitek.com:1" implementation=lio-t lun=3 path="/dev/drbd1004" allowed_initiators="iqn.1993-08.org.debian:01:1cc967493b4 iqn.1993-08.org.debian:01:181885d4e7d7" \
			        meta target-role=Started
			primitive vip IPaddr2 \
			        params ip=10.203.1.33 cidr_netmask=24 \
			        op monitor interval=10 timeout=20
			group g_linstor p_iscsi_portblock_on_drbd0 p_fs_linstordb p_linstor-controller vip iscsi_target_test seven ben test fred apple p_iscsi_portblock_off_drbd0
			ms ms_drbd_linstordb p_drbd_linstordb \
			        meta master-max=1 master-node-max=1 clone-max=2 clone-node-max=1 notify=true
			colocation c_linstor_with_drbd inf: g_linstor ms_drbd_linstordb:Master
			order o_drbd_before_linstor inf: ms_drbd_linstordb:promote g_linstor:start
			property cib-bootstrap-options: \
			        have-watchdog=false \
			        dc-version=1.1.14-70404b0 \
			        cluster-infrastructure=corosync \
			        cluster-name=debian \
			        stonith-enabled=false \
			        no-quorum-policy=ignore '''

		self.resstatu = '''+---------------------------------------------------------------------------------------------------------------+
| Node  | Resource  | StoragePool          | VolumeNr | MinorNr | DeviceName    | Allocated | InUse  |    State |
|===============================================================================================================|
| klay1 | apple     | pool_hdd             | 0        | 1000    | /dev/drbd1000 | 12 MiB    | InUse  | UpToDate |
| klay2 | apple     | DfltDisklessStorPool | 0        | 1000    | /dev/drbd1000 |           | Unused | Diskless |
| klay1 | banana    | pool_hdd             | 0        | 1001    | /dev/drbd1001 | 12 MiB    | InUse  | UpToDate |
| klay2 | banana    | pool_hdd             | 0        | 1001    | /dev/drbd1001 | 12 MiB    | Unused | UpToDate |
| klay1 | ben       | pool_hdd             | 0        | 1005    | /dev/drbd1005 | 12 MiB    | InUse  | UpToDate |
| klay2 | ben       | pool_hdd             | 0        | 1005    | /dev/drbd1005 | 12 MiB    | Unused | UpToDate |
| klay1 | fred      | pool_hdd             | 0        | 1003    | /dev/drbd1003 | 12 MiB    | InUse  | UpToDate |
| klay2 | fred      | pool_hdd             | 0        | 1003    | /dev/drbd1003 | 12 MiB    | Unused | UpToDate |
| klay1 | fst       | pool_hdd             | 0        | 1011    | /dev/drbd1011 | 1.00 GiB  | Unused | UpToDate |
| klay2 | fst       | pool_hdd             | 0        | 1011    | /dev/drbd1011 | 1.00 GiB  | Unused | UpToDate |
| klay1 | linstordb | pool_hdd             | 0        | 1002    | /dev/drbd1002 | 252 MiB   | InUse  | UpToDate |
| klay2 | linstordb | pool_hdd             | 0        | 1002    | /dev/drbd1002 | 252 MiB   | Unused | UpToDate |
| klay2 | pllo      | pllo                 | 0        | 1012    | None          |           | Unused |  Unknown |
| klay1 | seven     | pool_hdd             | 0        | 1006    | /dev/drbd1006 | 12 MiB    | InUse  | UpToDate |
| klay2 | seven     | pool_hdd             | 0        | 1006    | /dev/drbd1006 | 12 MiB    | Unused | UpToDate |
| klay1 | ssss      | pool_hdd             | 0        | 1009    | /dev/drbd1009 | 12 MiB    | Unused | UpToDate |
| klay1 | test      | pool_hdd             | 0        | 1004    | /dev/drbd1004 | 10.00 GiB | InUse  | UpToDate |
| klay2 | test      | pool_hdd             | 0        | 1004    | /dev/drbd1004 | 10.00 GiB | Unused | UpToDate |
| klay2 | xx2       | pool_hdd             | 0        | 1010    | /dev/drbd1010 | 12 MiB    | Unused | UpToDate |
+---------------------------------------------------------------------------------------------------------------+'''

	def re_data(self):
		plogical = re.compile(r'primitive\s(\w*)\s\w*\s\\\s*\w*\starget_iqn="([a-zA-Z0-9.:-]*)"\s[a-z=-]*\slun=(\d*)\spath="([a-zA-Z0-9/]*)"\sallowed_initiators="([a-zA-Z0-9.: -]+)"(?:.*\s*){2}meta target-role=(\w*)')
		pvip = re.compile(r'primitive\s(\w*)\sIPaddr2\s\\\s*\w*\sip=([0-9.]*)\s\w*=(\d*)\s')
		ptarget = re.compile(r'primitive\s(\w*)\s\w*\s\\\s*params\siqn="([a-zA-Z0-9.:-]*)"\s[a-z=-]*\sportals="([0-9.]*):\d*"\s\\')
		redata = [plogical.findall(self.iscsistatu), pvip.findall(self.iscsistatu), ptarget.findall(self.iscsistatu)]
		return redata
		# print(plogical.findall(iscsistatu))
		# print(pvip.findall(iscsistatu))
		# print(ptarget.findall(iscsistatu))

		# strlogical=plogical.findall(iscsistatu)
		# sdict = {}
		# for s in strlogical:
		# 	sdict.update({"iqn":s[1]})
			#sdict.update({})
		# print(sdict)

	def lsdata(self):
		linstordata = self.resstatu
		return linstordata

	def get_data(self):
		crmconfig = subprocess.check_output('crm configure show',shell=True)
		linstorres = subprocess.getoutput('linstor --no-color --no-utf8 r lv', shell=True)





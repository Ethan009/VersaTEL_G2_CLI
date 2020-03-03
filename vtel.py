#coding:utf-8

import argparse
import sys
import Process
from LINSTOR_CLI import LINSTOR_action as la


class CLI():
    def __init__(self):
        self.parser_vtel()
        self.parser_stor()
        self.parser_iscsi()
        self.args = self.vtel.parse_args()
        self.judge()


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
        sub_vtel_stor = self.vtel_stor.add_subparsers(dest='stor_sub')
        self.stor_node = sub_vtel_stor.add_parser('node', aliases='n', help='Management operations for node')
        self.stor_resource = sub_vtel_stor.add_parser('resource', aliases='r', help='Management operations for storagepool')
        self.stor_storagepool = sub_vtel_stor.add_parser('storagepool', aliases=['sp'],help='Management operations for storagepool')
        self.stor_snap = sub_vtel_stor.add_parser('snap', aliases=['sn'], help='Management operations for snapshot')

        ###node
        sub_stor_node = self.stor_node.add_subparsers(dest='node_sub')
        self.node_create = sub_stor_node.add_parser('create', aliases='c', help='Create the node')
        self.node_modify = sub_stor_node.add_parser('modify', aliases='m', help='Modify the node')
        self.node_delete = sub_stor_node.add_parser('delete', aliases='d', help='Delete the node')
        self.node_show = sub_stor_node.add_parser('show', aliases='s', help='Displays the node view')

        ###resource
        stor_resource = self.stor_resource.add_subparsers(dest='resource_sub')
        self.resource_create = stor_resource.add_parser('create', aliases='c', help='Create the resource')  # usage =
        self.resource_modify = stor_resource.add_parser('modify', aliases='m',help='Modify the resource')
        self.resource_delete = stor_resource.add_parser('delete', aliases='d',help='Delete the resource')
        self.resource_show = stor_resource.add_parser('show', aliases='s', help='Displays the resource view')

        ###storagepool
        sub_stor_storagepool = self.stor_storagepool.add_subparsers(dest='storagepool_sub')
        self.storagepool_create = sub_stor_storagepool.add_parser('create', aliases='c',help='Create the storagpool')
        self.storagepool_modify = sub_stor_storagepool.add_parser('modify', aliases='m',help='Modify the storagpool')
        self.storagepool_delete = sub_stor_storagepool.add_parser('delete', aliases='d',help='Delete the storagpool')
        self.storagepool_show = sub_stor_storagepool.add_parser('show', aliases='s',help='Displays the storagpool view')

        ###snap
        sub_stor_snap = self.stor_snap.add_subparsers(dest='snap_sub')
        self.snap_create = sub_stor_snap.add_parser('create', help='Create the snapshot')
        self.snap_modify = sub_stor_snap.add_parser('modify', help='Modify the snapshot')
        self.snap_delete = sub_stor_snap.add_parser('delete', help='Delete the snapshot')
        self.snap_show = sub_stor_snap.add_parser('show', help='Displays the snapshot view')

        ###stor node create
        self.node_create.add_argument('node', metavar='NODE', action='store', help='node name')
        self.node_create.add_argument('-ip', dest='ip', action='store', help='ip', required=True)
        self.node_create.add_argument('-nt', dest='nodetype', action='store', help='node type:Combined/...',required=True)

        ###stor node modify

        ###stor node delete
        self.node_delete.add_argument('node', action='store', help='node name')

        ###stor node show
        self.node_show.add_argument('node', help='Show Node view', action='store', nargs='?', default=None)

        ###stor resource create

        self.resource_create.add_argument('resource', action='store',help='define resource name to be created.')
        self.resource_create.add_argument('-s', dest='size', action='store',help='define resource size to be created.In addition to creating diskless resource, you must enter SIZE')

        group_auto = self.resource_create.add_argument_group(title='auto create')
        group_auto.add_argument('-a', dest='auto', action='store_true', default=False,help='choose to create automatically')
        group_auto.add_argument('-num', dest='num', action='store', help='specify the quantity', type=int)

        group_manual = self.resource_create.add_argument_group(title='manual create')
        group_manual.add_argument('-n', dest='node', action='store', help='specify the node of the resource')
        group_manual.add_argument('-sp', dest='storagepool', help='create storagepool')

        group_manual_diskless = self.resource_create.add_argument_group(title='diskless create')
        group_manual_diskless.add_argument('-diskless', action='store_true', default=False, dest='diskless',help='diskless')

        ###stor resource modify
        self.resource_modify.add_argument('resource',action='store', help='resources to be modified')
        self.resource_modify.add_argument('-n', dest='node', action='store', help='node to be modified')
        self.resource_modify.add_argument('-sp', dest='storagepool', action='store', help='Storagepool')

        ###stor resource delete
        self.resource_delete.add_argument('resource', action='store', help='the resource to delete')
        self.resource_delete.add_argument('-n', dest='node', action='store', help='the node to delete')
        self.resource_delete.add_argument('-y', dest='yes', action='store_true',help='Skip to confirm selection', default=False)

        ###stor resource show
        self.resource_show.add_argument('resource', help='Show Resource view', action='store', nargs='?')

        ###stor storagepool create
        self.storagepool_create.add_argument('storagepool', action='store', help='storagepool name')
        self.storagepool_create.add_argument('-n', dest='node', action='store', help='node name')
        group_type = self.storagepool_create.add_mutually_exclusive_group()
        group_type.add_argument('-lvm', dest='lvm', action='store', help='vg name')
        group_type.add_argument('-tlv', dest='tlv', action='store', help='thinlv name')

        ###stor storagepool modify

        ###stor storagepool delete
        self.storagepool_delete.add_argument('storagepool', help='storagepool name', action='store')
        self.storagepool_delete.add_argument('-n', dest='node', action='store', help='node name')
        self.storagepool_delete.add_argument('-y', dest='yes', action='store_true',help='Skip to confirm selection', default=False)

        ###stor storgagepool show
        self.storagepool_show.add_argument('storagepool', help='Show Storagepool view', action='store',nargs='?')

        ###stor snap create

        ###stor snap modify

        ###stor snap delete

        ###stor snap show

    def parser_iscsi(self):
        ##iscsi
        sub_vtel_iscsi = self.vtel_iscsi.add_subparsers(dest='iscsi_next')
        self.vtel_iscsi_create = sub_vtel_iscsi.add_parser('create', help='iscsi resource create...', add_help=False)
        self.vtel_iscsi_show = sub_vtel_iscsi.add_parser('show', help='iscsi resource modify...', add_help=False)
        self.vtel_iscsi_modify = sub_vtel_iscsi.add_parser('modify', help='iscsi resource create...', add_help=False)
        self.vtel_iscsi_delete = sub_vtel_iscsi.add_parser('delete', help='iscsi resource modify...', add_help=False)





    def case_node(self):
        args = self.args
        parser_create = self.node_create
        parser_delete = self.node_delete

        def node_create():
            if args.node and args.nodetype and args.ip:
                la.linstor_create_node(args.node, args.ip, args.nodetype)
            else:
                parser_create.print_help()

        def node_modify():
            pass

        def node_delete():
            if args.node:
                if la.confirm_del():
                    la.linstor_delete_node(args.node)
            else:
                parser_delete.print_help()

        def node_show():
            tb = Process.Table_show()
            tb.run()
            if args.node:
                tb.node_one(args.node)
            else:
                tb.node_all()


        if self.args.node_sub in ['create','c']:
            node_create()
        elif self.args.node_sub in ['modify','m']:
            node_modify()
        elif self.args.node_sub in ['delete','d']:
            node_delete()
        elif self.args.node_sub in ['show','s']:
            node_show()
        else:
            self.stor_node.print_help()

    def case_resource(self):
        args = self.args
        parser_create = self.resource_create
        parser_modify = self.resource_modify
        parser_delete = self.resource_delete


        def resource_create():
            if args.size:
                if all([args.auto, args.num]) and not any([args.node, args.storagepool, args.diskless]):
                    la.linstor_create_res_auto(args.resource, args.size, args.num)
                elif all([args.node, args.storagepool]) and not any([args.auto, args.num, args.diskless]):
                    la.linstor_create_res_manual(args.resource, args.size, args.node, args.storagepool)
                else:
                    parser_create.print_help()
            elif args.diskless:
                if args.node and not any([args.auto, args.num, args.storagepool]):
                    la.linstor_create_res_diskless(args.node, args.resource)
                else:
                    parser_create.print_help()
            else:
                parser_create.print_help()

            #     print('E.g.')
            #     print('自动创建：vtel stor create RESOURCE -s SIZE -a -num NUM')
            #     print('手动创建：vtel stor create RESOURCE -s SIZE -n NODE -sp STORAGEPOOL')
            #     print('创建diskless：vtel stor create RESOURCE -diskless NODE')

        def resource_modify():
            if args.resource:
                if args.size:
                    print('调整resource的size')
                elif args.node and args.diskless:
                    print('将某节点上某个diskful的资源调整为diskless')

                elif args.node and args.storagepool:
                    print('将某节点上某个diskless的资源调整为diskful')
            else:
                parser_modify.print_help()

        def resource_delete():
            if args.resource:
                if args.node:
                    if args.yes:
                        la.linstor_delete_resource_des(args.node, args.resource)
                    else:
                        if la.confirm_del():
                            la.linstor_delete_resource_des(args.node, args.resource)
                elif not args.node:
                    if args.yes:
                        la.linstor_delete_resource_all(args.resource)
                    else:
                        if la.confirm_del():
                            la.linstor_delete_resource_all(args.resource)
            else:
                parser_delete.print_help()

        def resource_show():
            tb = Process.Table_show()
            tb.run()
            if args.resource:
                tb.resource_one(args.resource)
            else:
                tb.resource_all()

        if args.resource_sub in ['create','c']:
            resource_create()
        elif args.resource_sub == ['modify','m']:
            resource_modify()
        elif args.resource_sub == ['delete','d']:
            resource_delete()
        elif args.resource_sub == ['show','s']:
            resource_show()
        else:
            self.stor_resource.print_help()

    def case_storagepool(self):
        args = self.args
        parser_create = self.storagepool_create
        parser_modify = self.storagepool_modify
        parser_delete = self.storagepool_delete

        def storagepool_create():
            if args.storagepool and args.node:
                if args.lvm:
                    la.linstor_create_storagepool_lvm(args.node, args.storagepool, args.lvm)
                elif args.tlv:
                    la.linstor_create_storagepool_thinlv(args.node, args.storagepool, args.tlv)
                else:
                    parser_create.print_help()
            else:
                parser_create.print_help()


        def storagepool_modify():
            pass


        def storagepool_delete():
            if args.storagepool:
                if args.node:
                    if args.yes:
                        la.linstor_delete_storagepool(args.node, args.storagepool)
                    else:
                        if la.confirm_del():
                            la.linstor_delete_storagepool(args.node, args.storagepool)
                else:
                    parser_delete.print_help()
            else:
                parser_delete.print_help()

        def storagepool_show():
            tb = Process.Table_show()
            tb.run()
            if args.storagepool:
                tb.storagepool_one(args.storagepool)
            else:
                tb.storagepool_all()


        if args.storagepool_sub in ['create','c']:
            storagepool_create()
        elif args.storagepool_sub in ['modify','m']:
            storagepool_modify()
        elif args.storagepool_sub in ['delete','d']:
            storagepool_delete()
        elif args.storagepool_sub in ['show','s']:
            storagepool_show()
        else:
            self.stor_storagepool.print_help()

    #pass
    def case_snap(self):
        args = self.args
        parser = self.storagepool_create

        def snap_create():
            args = self.args
            parser = self.storagepool_create

            if args.storagepool and args.node:
                if args.lvm:
                    la.linstor_create_storagepool_lvm(args.node, args.storagepool, args.lvm)
                elif args.tlv:
                    la.linstor_create_storagepool_thinlv(args.node, args.storagepool, args.tlv)
            else:
                parser.print_help()

        def snap_modify():
            pass

        def snap_delete():
            pass

        def snap_show():
            pass


        if self.args.snap_sub == 'create':
            snap_create()
        elif self.args.snap_sub == 'modify':
            snap_modify()
        elif self.args.snap_sub == 'delete':
            snap_delete()
        elif self.args.snap_sub == 'show':
            snap_show()
        else:
            self.stor_snap.print_help()


    def judge(self):
        if self.args.vtel_sub == 'stor':
            if self.args.stor_sub in ['node','n']:
                self.case_node()
            elif self.args.stor_sub in ['resource','r']:
                self.case_resource()
            elif self.args.stor_sub in ['storagepool','sp']:
                self.case_storagepool()
            elif self.args.stor_sub in ['snap','sn']:
                self.case_snap()
            else:
                self.vtel_stor.print_help()

        elif 'iscsi' in sys.argv:
            if 'show' in sys.argv:
                pass

        else:
            self.vtel.print_help()

if __name__ == '__main__':
    CLI()


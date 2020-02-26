#coding:utf-8

import argparse
import sys
import Process
from LINSTOR_CLI import LINSTOR_action as la


class CLI():
    def __init__(self):
        self.parser_first()
        self.parser_second()
        self.parser_thrid()
        self.stor_arg()
        self.iscsi_arg()
        self.vtel_help()
        self.args = self.vtel.parse_args()
        self.judge()


    def parser_first(self):
        self.vtel = argparse.ArgumentParser(prog='vtel',formatter_class=argparse.RawTextHelpFormatter, add_help=False)
        sub_vtel = self.vtel.add_subparsers(dest='vtel_next')

        # add all sub parse
        self.vtel_stor = sub_vtel.add_parser('stor',help='for storage resource management...',add_help=False)
        self.vtel_iscsi = sub_vtel.add_parser('iscsi',help='for iscsi resource management...',add_help=False)
        self.vtel_fc = sub_vtel.add_parser('fc',help='for fc resource management...',add_help=False)
        self.vtel_ceph = sub_vtel.add_parser('ceph',help='for ceph resource management...',add_help=False)

    def parser_second(self):
        ##stor
        sub_vtel_stor = self.vtel_stor.add_subparsers(dest='stor_next')
        self.vtel_stor_node = sub_vtel_stor.add_parser('node', help='node operation')
        self.vtel_stor_resource = sub_vtel_stor.add_parser('resource', help='resource operation')
        self.vtel_stor_storagepool = sub_vtel_stor.add_parser('storagepool', help='storagepool operation')
        self.vtel_stor_snap = sub_vtel_stor.add_parser('snap', help='snap operation')

        ##iscsi
        sub_vtel_iscsi = self.vtel_iscsi.add_subparsers(dest='iscsi_next')
        self.vtel_iscsi_create = sub_vtel_iscsi.add_parser('create',help='iscsi resource create...', add_help=False)
        self.vtel_iscsi_show = sub_vtel_iscsi.add_parser('show',help='iscsi resource modify...', add_help=False)
        self.vtel_iscsi_modify = sub_vtel_iscsi.add_parser('modify',help='iscsi resource create...', add_help=False)
        self.vtel_iscsi_delete = sub_vtel_iscsi.add_parser('delete',help='iscsi resource modify...', add_help=False)


    def parser_thrid(self):
        ###node
        sub_vtel_stor_node = self.vtel_stor_node.add_subparsers(dest='node_next')
        self.vtel_stor_node_create = sub_vtel_stor_node.add_parser('create',help='node create')
        self.vtel_stor_node_modify = sub_vtel_stor_node.add_parser('modify', help='node modify')
        self.vtel_stor_node_delete = sub_vtel_stor_node.add_parser('delete', help='node delete')
        self.vtel_stor_node_show = sub_vtel_stor_node.add_parser('show', help='node show')


        ###resource
        sub_vtel_stor_resource = self.vtel_stor_resource.add_subparsers(dest='resource_next')
        self.vtel_stor_resource_create = sub_vtel_stor_resource.add_parser('create', help='resource create')
        self.vtel_stor_resource_modify = sub_vtel_stor_resource.add_parser('modify',help='resource modify')
        self.vtel_stor_resource_delete = sub_vtel_stor_resource.add_parser('delete', help='resource delete')
        self.vtel_stor_resource_show = sub_vtel_stor_resource.add_parser('show', help='resource show')


        ###storagepool
        sub_vtel_stor_storagepool = self.vtel_stor_storagepool.add_subparsers(dest='storagepool_next')
        self.vtel_stor_storagepool_create = sub_vtel_stor_storagepool.add_parser('create', help='storagepool create')
        self.vtel_stor_storagepool_modify = sub_vtel_stor_storagepool.add_parser('modify',help='storagepool modify')
        self.vtel_stor_storagepool_delete = sub_vtel_stor_storagepool.add_parser('delete', help='storagepool delete')
        self.vtel_stor_storagepool_show = sub_vtel_stor_storagepool.add_parser('show', help='storagepool show')


        ###snap
        sub_vtel_stor_snap = self.vtel_stor_snap.add_subparsers(dest='snap_next')
        self.vtel_stor_snap_create = sub_vtel_stor_snap.add_parser('create',help='snap create')
        self.vtel_stor_snap_modify = sub_vtel_stor_snap.add_parser('modify',help='snap modify')
        self.vtel_stor_snap_delete = sub_vtel_stor_snap.add_parser('delete', help='snap delete')
        self.vtel_stor_snap_show = sub_vtel_stor_snap.add_parser('show', help='snap show')


    def stor_arg(self):
        ###stor node create
        self.vtel_stor_node_create.add_argument('node',metavar='NODE',action='store',help='node name')
        self.vtel_stor_node_create.add_argument('-ip', dest='ip',action='store', help='ip')
        self.vtel_stor_node_create.add_argument('-nt', dest='nodetype',action='store',help='node type:Combined/Controller/Auxiliary/Satellite')

        ###stor node modify

        ###stor node delete
        self.vtel_stor_node_delete.add_argument('node',metavar='NODE',action='store',help='node name')

        ###stor node show
        self.vtel_stor_node_show.add_argument('node',metavar='NODE',help='Show Node view', action='store',nargs='?',default=None)


        ###stor resource create

        self.vtel_stor_resource_create.add_argument('resource',metavar='RESOURCE',action='store',help='define resource name to be created.')
        self.vtel_stor_resource_create.add_argument('-s',dest='size',action='store',help='define resource size to be created.In addition to creating diskless resource, you must enter SIZE')

        group_auto = self.vtel_stor_resource_create.add_argument_group(title='auto create')
        group_manual = self.vtel_stor_resource_create.add_argument_group(title='manual create')
        group_manual_diskless = self.vtel_stor_resource_create.add_argument_group(title='diskless create')

        group_auto.add_argument('-a', dest='auto',action='store_true', default=False,help='choose to create automatically')
        group_auto.add_argument('-num',dest='num',action='store',help='specify the quantity',type=int)
        group_manual.add_argument('-n',dest='node',action='store',help='specify the node of the resource')
        group_manual.add_argument('-sp', dest='storagepool',help='create storagepool')

        #group_manual_diskless.add_argument('-n',dest='node',action='store',help='specify the node of the resource')
        group_manual_diskless.add_argument('-diskless',action='store_true',default=False,dest='diskless',help='diskless')

        ###stor resource modify
        self.vtel_stor_resource_modify.add_argument('resource',metavar='RESOURCE',action='store',help='resources to be modified')
        self.vtel_stor_resource_modify.add_argument('-n',dest='node',action='store',help='node to be modified')
        self.vtel_stor_resource_modify.add_argument('-sp',dest='storagepool',action='store',help='Storagepool')
        self.vtel_stor_resource_modify.add_argument('-s',dest='size',action='store',help='size')
        self.vtel_stor_resource_modify.add_argument('-diskless',action='store_true',default=False,dest='diskless',help='diskless')
        #self.vtel_stor_resource_modify.add_argument('-rollback',dest='rollback',help='snapshot rollback,used with \'-snap\'')
        #self.vtel_stor_resource_modify.add_argument('-snap',dest='snap',help='select the snapshot to roll back,used with \'-rollback\'')

        ###stor resource delete
        self.vtel_stor_resource_delete.add_argument('resource',metavar='RESOURCE',action='store',help='the resource to delete')
        self.vtel_stor_resource_delete.add_argument('-n',dest='node',action='store',help='the node to delete')
        self.vtel_stor_resource_delete.add_argument('-y',dest='yes',action='store_true',help='Skip to confirm selection',default=False)

        ###stor resource show
        self.vtel_stor_resource_show.add_argument('resource',help='Show Resource view',action='store', nargs='?')

        ###stor storagepool create
        self.vtel_stor_storagepool_create.add_argument('storagepool',metavar='STORAGEPOOL',action='store',help='storagepool name')
        self.vtel_stor_storagepool_create.add_argument('-n',dest='node',action='store',help='node name')
        group_type = self.vtel_stor_storagepool_create.add_mutually_exclusive_group()
        group_type.add_argument('-lvm',dest='lvm',action='store',help='vg name')
        group_type.add_argument('-tlv',dest='tlv',action='store',help='thinlv name')

        ###stor storagepool modify


        ###stor storagepool delete
        self.vtel_stor_storagepool_delete.add_argument('storagepool', metavar='STORAGEPOOL',help='storagepool name',action='store')
        self.vtel_stor_storagepool_delete.add_argument('-n',dest='node',action='store',help='node name')
        self.vtel_stor_storagepool_delete.add_argument('-y', dest='yes', action='store_true',
                                                    help='Skip to confirm selection', default=False)

        ###stor storgagepool show
        self.vtel_stor_storagepool_show.add_argument('storagepool',metavar='STORAGEPOOL', help='Show Storagepool view', action='store', nargs='?')


        ###stor snap create

        ###stor snap modify

        ###stor snap delete

        ###stor snap show





    def iscsi_arg(self):

        ### iscsi create

        self.vtel_iscsi_create.add_argument('-h',dest='host',action='store',help='host')
        self.vtel_iscsi_create.add_argument('-hg',dest='host_group',action='store',help='host group')
        self.vtel_iscsi_create.add_argument('-dg',dest='drive_group',action='store',help='driver group')
        self.vtel_iscsi_create.add_argument('-m',dest='map',action='store',help='mapping')
        self.vtel_iscsi_create.add_argument('-mem',dest='member',action='store',help='member')
        self.vtel_iscsi_create.add_argument('-lid', dest='lun_id', action='store', help='member',type=int)
        # --path
        # --al(输入INITIATOR，获取iqn)
        # -target（输入target获取target iqn）


        ### iscsi show
        group_iscsi_show = self.vtel_iscsi_show.add_mutually_exclusive_group(required=False)
        group_iscsi_show.add_argument('-h',dest='host',action='store',help='host',nargs='?',const='-h',default=None)
        group_iscsi_show.add_argument('-hg',dest='host_group',action='store',help='host group',nargs='?',const='-hg',default=None)
        group_iscsi_show.add_argument('-rg',dest='resource_group',action='store',help='resource group',nargs='?',const='-rg',default=None)
        group_iscsi_show.add_argument('-r',dest='resource',action='store',help='resource',nargs='?',const='-r',default=None)
        group_iscsi_show.add_argument('-m',dest='member',action='store',help='member',nargs='?',const='-m',default=None)


#iscsi
    def vtel_help(self):
        if len(sys.argv) == 1:
            # display help message when no args are passed.
            self.vtel.print_help()
            sys.exit(1)



    def stor_node_create(self):
        args = self.args
        parser = self.vtel_stor_node_create

        if args.node and args.nodetype and args.ip:
            la.linstor_create_node(args.node,args.ip,args.nodetype)
        else:
            parser.print_help()

    def stor_node_modify(self):
        pass

    def stor_node_delete(self):
        args = self.args
        parser = self.vtel_stor_node_delete

        if args.node:
            if la.confirm_del():
                la.linstor_delete_node(args.node)
        else:
            parser.print_help()

    def stor_node_show(self):
        args = self.args
        tb = Process.Table_show()
        tb.run()
        if args.node:
            tb.node_one(args.node)
        else:
            tb.node_all()


    def stor_resource_create(self):
        args = self.args
        parser = self.vtel_stor_resource_create

        #创建resource
        if args.size:
            if args.auto:
                if args.node:
                    print('自动创建不需要-n，手动创建不需要-a')
                elif args.storagepool:
                    print('自动创建不需要-sp')
                elif args.diskless:
                    print('自动创建不需要-diskless')
                elif args.num:
                    la.linstor_create_res_auto(args.resource,args.size,args.num)
                else:
                    print('自动创建需要还需要-num')#提示

            elif args.storagepool and args.node:
                if args.num:
                    print('手动创建不需要-num')

                elif args.diskless:
                    print('手动创建不需要-diskless，创建diskless不需要-s,-n和-sp')
                else:
                    la.linstor_create_res_manual(args.resource,args.size,args.node,args.storagepool)

            elif args.node:
                if args.num:
                    print('手动创建不需要-num，并且还需要-sp')
                elif args.diskless:
                    print('手动创建不需要-diskless')
                else:
                    print('手动创建还需要-sp')

            elif args.storagepool:
                if args.num:
                    print('手动创建不需要-num,并且还需要-n')
                elif args.diskless:
                    print('手动创建不需要-diskless')
                else:
                    print('手动创建还需要-n')

            else:
                print('''请选择创建方式：
                自动创建:-a -num NUM
                手动创建:-n NODE -sp STORAGEPOOL
                ''')

        elif args.diskless:
            if args.auto:
                print('创建diskless不需要-a')
            elif args.num:
                print('创建diskless不需要-num')
            elif args.storagepool:
                print('创建diskless不需要-sp')
            elif args.node:
                la.linstor_create_res_diskless(args.node,args.resource)
            else:
                print('创建diskless资源需要-n')


        else:
            parser.print_help()
            print('E.g.')
            print('自动创建：vtel stor create RESOURCE -s SIZE -a -num NUM')
            print('手动创建：vtel stor create RESOURCE -s SIZE -n NODE -sp STORAGEPOOL')
            print('创建diskless：vtel stor create RESOURCE -diskless NODE')

    def stor_resource_modify(self):
        args = self.args
        parser_stor_modify = self.vtel_stor_resource_modify

        if args.resource:
            if args.size:
                print('调整resource的size')
            elif args.node and args.diskless:
                print('将某节点上某个diskful的资源调整为diskless')

            elif args.node and args.storagepool:
                print('将某节点上某个diskless的资源调整为diskful')
        else:
            parser_stor_modify.print_help()

    def stor_resource_delete(self):
        args = self.args
        parser_stor_delete = self.vtel_stor_resource_delete


        if args.resource:
            if args.node:
                if args.yes:
                    la.linstor_delete_resource_des(args.node,args.resource)
                else:
                    if la.confirm_del():
                        la.linstor_delete_resource_des(args.node,args.resource)

            elif not args.node:
                if args.yes:
                    la.linstor_delete_resource_all(args.resource)
                else:
                    if la.confirm_del():
                        la.linstor_delete_resource_all(args.resource)
                    # else:
                    #     print('Operation canceled')
        else:
            parser_stor_delete.print_help()

    def stor_resource_show(self):
        args = self.args
        tb = Process.Table_show()
        tb.run()
        if args.resource:
            tb.resource_one(args.resource)
        else:
            tb.resource_all()


    def stor_storagepool_create(self):
        args = self.args
        parser = self.vtel_stor_storagepool_create

        if args.storagepool and args.node:
            if args.lvm:
                la.linstor_create_storagepool_lvm(args.node,args.storagepool,args.lvm)
            elif args.tlv:
                la.linstor_create_storagepool_thinlv(args.node,args.storagepool,args.tlv)
            else:
                print('缺少指定lvm/thin lv')
        else:
            parser.print_help()


    def stor_storagepool_modify(self):
        pass

    def stor_storagepool_delete(self):
        args = self.args
        parser = self.vtel_stor_storagepool_delete

        if args.storagepool:
            if args.node:
                if args.yes:
                    la.linstor_delete_storagepool(args.node,args.storagepool)
                else:
                    if la.confirm_del():
                        la.linstor_delete_storagepool(args.node,args.storagepool)
            else:
                print('缺少指定节点 -n')
        # elif args.node:
        #     if args.storagepool:
        #         if args.yes:
        #             print('直接删除指定节点的指定存储池')
        #         else:
        #             print('删除指定节点的指定存储池')
        #             LC.LINSTOR_action.confirm_res_del()
        #     else:
        #         print('缺少指定存储池 -sp')
        else:
            parser.print_help()




    def stor_storagepool_show(self):
        args = self.args
        tb = Process.Table_show()
        tb.run()
        if args.storagepool:
            tb.storagepool_one(args.storagepool)
        else:
            tb.storagepool_all()


    def stor_snap_create(self):
        args = self.args
        parser = self.vtel_stor_storagepool_create

        if args.storagepool and args.node:
            if args.lvm:
                la.linstor_create_storagepool_lvm(args.node,args.storagepool,args.lvm)
            elif args.tlv:
                la.linstor_create_storagepool_thinlv(args.node,args.storagepool,args.tlv)
        else:
            parser.print_help()


    def stor_snap_modify(self):
        pass

    def stor_snap_delete(self):
        pass

    def stor_snap_show(self):
        pass


    def iscsi_show(self):
        args = self.args
        parser_iscsi_show = self.vtel_iscsi_show

        if args.host == '-h':
            print('all host')
        elif args.host:
            print('one host')

        elif args.host_group == '-hg':
            print('all host group')
        elif args.host_group:
            print('one host group')

        elif args.resource == '-r':
            print('all resource')
        elif args.resource:
            print('one resource')

        elif args.resource_group == '-rg':
            print('all resource group')
        elif args.resource_group:
            print('one resource group')

        elif args.member == '-m':
            print('all member')
        elif args.member:
            print('one member')
        else:
            parser_iscsi_show.print_help()



    def judge_node(self):

        if self.args.node_next == 'create':
            self.stor_node_create()
        elif self.args.node_next == 'modify':
            self.stor_node_modify()
        elif self.args.node_next == 'delete':
            self.stor_node_delete()
        elif self.args.node_next == 'show':
            self.stor_node_show()
        else:
            self.vtel_stor_node.print_help()

    def judge_resource(self):
        if self.args.resource_next == 'create':
            self.stor_resource_create()
        elif self.args.resource_next == 'modify':
            self.stor_resource_modify()
        elif self.args.resource_next == 'delete':
            self.stor_resource_delete()
        elif self.args.resource_next == 'show':
            self.stor_resource_show()
        else:
            self.vtel_stor_resource.print_help()


    def judge_storagepool(self):
        if self.args.storagepool_next == 'create':
            self.stor_storagepool_create()
        elif self.args.storagepool_next == 'modify':
            self.stor_storagepool_modify()
        elif self.args.storagepool_next == 'delete':
            self.stor_storagepool_delete()
        elif self.args.storagepool_next == 'show':
            self.stor_storagepool_show()
        else:
            self.vtel_stor_storagepool.print_help()

    def judge_snap(self):
        if self.args.snap_next == 'create':
            self.stor_snap_create()
        elif self.args.snap_next == 'modify':
            self.stor_snap_modify()
        elif self.args.snap_next == 'delete':
            self.stor_snap_delete()
        elif self.args.snap_next == 'show':
            self.stor_snap_show()
        else:
            self.vtel_stor_snap.print_help()




    def judge(self):
        if self.args.vtel_next == 'stor':
            if self.args.stor_next == 'node':
                self.judge_node()
            elif self.args.stor_next == 'resource':
                self.judge_resource()
            elif self.args.stor_next == 'storagepool':
                self.judge_storagepool()
            elif self.args.stor_next == 'snap':
                self.judge_snap()
            else:
                self.vtel_stor.print_help()

        elif 'iscsi' in sys.argv:
            if 'show' in sys.argv:
                self.iscsi_show()

        else:
            self.vtel.print_help()

if __name__ == '__main__':
    args = CLI()
    # if args.stor == 'create':
    #     stor_create(args.resource, args.size, args.auto, args.num, args.node, args.storagepool, args.diskless)
    # elif args.stor == 'show':
    #     stor_show(args.node,args.resource,args.storagepool)


#coding:utf-8
import subprocess
import regex as reg



def execute_cmd(cmd):
    action = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = action.stdout
    if reg.judge_cmd_result_err(str(result)):
        print(result.decode('utf-8'))
    elif reg.judge_cmd_result_war(str(result)):
        print(result.decode('utf-8'))
    elif reg.judge_cmd_result_suc(str(result)):
        return True





class LINSTOR_action():


    #创建resource相关 -- ok
    @staticmethod
    def linstor_delete_rd(res):
        cmd = 'linstor rd d %s'%res
        subprocess.check_output(cmd,shell=True)

    @staticmethod
    def linstor_delete_vd(res):
        cmd = 'linstor vd d %s' %res
        subprocess.check_output(cmd,shell=True)


    @staticmethod
    def linstor_create_rd(res):
        cmd_rd = 'linstor rd c %s' %res
        return execute_cmd(cmd_rd)

    @staticmethod
    def linstor_create_vd(res,size):
        cmd_vd = 'linstor vd c %s %s' % (res, size)
        if execute_cmd(cmd_vd):
            return True
        else:
            LINSTOR_action.linstor_delete_rd(res)

    #创建resource 自动
    @staticmethod
    def linstor_create_res_auto(res,size,num):
        cmd = 'linstor r c %s --auto-place %d' % (res, num)
        if LINSTOR_action.linstor_create_rd(res) and LINSTOR_action.linstor_create_vd(res,size):
            if execute_cmd(cmd):
                print('SUCESS')
            else:
                LINSTOR_action.linstor_delete_rd(res)


    #创建resource 手动
    @staticmethod
    def linstor_create_res_manual(res,size,node,stp):
        flag = 0

        def whether_delete_rd():
            if flag == len(node):
                LINSTOR_action.linstor_delete_rd(res)


        def create_resource():
            if execute_cmd(cmd):
                print('Resource %s was successfully created on Node %s'%(res,node_one))
            else:
                return flag+1


        if len(stp) == 1:
            if LINSTOR_action.linstor_create_rd(res) and LINSTOR_action.linstor_create_vd(res, size):
                for node_one in node:
                    cmd = 'linstor resource create %s %s --storage-pool %s' % (node_one, res, stp[0])
                    print (cmd)
                    create_resource()
                    whether_delete_rd()
        elif len(node) == len(stp):
            if LINSTOR_action.linstor_create_rd(res) and LINSTOR_action.linstor_create_vd(res, size):
                for node_one,stp_one in zip(node,stp):
                    cmd = 'linstor resource create %s %s --storage-pool %s' % (node_one, res, stp_one)
                    create_resource()
                    whether_delete_rd()


        # if LINSTOR_action.linstor_create_rd(res) and LINSTOR_action.linstor_create_vd(res,size):
            # action = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # result = action.stdout
            # if reg.judge_cmd_result_suc(str(result)):
            #     print('SUCCESS')
            # elif reg.judge_cmd_result_err(str(result)):
            #     LINSTOR_action.linstor_delete_rd(res)
            #     print('Fail')
            #     print(result.decode('utf-8'))



    #添加mirror（自动）
    @staticmethod
    def add_mirror_auto(res,num):
        cmd = 'linstor r c %s --auto-place %d' % (res, num)
        action = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        result = action.stdout
        if reg.judge_cmd_result_err(str(result)):
            print('Fail')
            print(result.decode('utf-8'))
        elif reg.judge_cmd_result_suc(str(result)):
            print('SUCCESS')
            return True

    @staticmethod
    def add_mirror_manual(res,node,stp):
        def add_mirror():
            action = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            result = action.stdout
            if reg.judge_cmd_result_suc(str(result)):
                print('Resource %s was successfully created on Node %s') %(res,node_one)
            elif reg.judge_cmd_result_err(str(result)):
                print('Fail')
                print(result.decode('utf-8'))


        if len(stp) == 1:
            for node_one in node:
                cmd = 'linstor resource create %s %s --storage-pool %s' % (node_one, res, stp[0])
                print(cmd)
                add_mirror()
        elif len(node) == len(stp):
            for node_one,stp_one in zip(node,stp):
                cmd = 'linstor resource create %s %s --storage-pool %s' % (node_one, res, stp_one)
                print(cmd)
                add_mirror()
        else:
            print('sp数量为1或者与node相等')



    #创建resource --diskless
    @staticmethod
    def linstor_create_res_diskless(node,res):
        cmd = 'linstor r c %s %s --diskless' %(node,res)
        action = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        result = action.stdout
        if reg.judge_cmd_result_err(str(result)):
            print('Fail')
            # print('Cause:')
            # print(reg.get_err_mes(str(result)))
            print(result.decode('utf-8'))
        elif reg.judge_cmd_result_suc(str(result)):
            print('SUCCESS')
            return True

    #删除resource,指定节点 -- ok
    @staticmethod
    def linstor_delete_resource_des(node,res):
        cmd = 'linstor resource delete %s %s' %(node,res)
        action = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = action.stdout
        if reg.judge_cmd_result_err(str(result)):
            print('Fail')
            # print('Cause:')
            # print(reg.get_err_mes(str(result)))
            print(result.decode('utf-8'))
        elif reg.judge_cmd_result_war(str(result)):
            print('Fail')
            print(result.decode('utf-8'))
        elif reg.judge_cmd_result_suc(str(result)):
            print('SUCCESS')
            return True

    #删除resource，全部节点 -- ok
    @staticmethod
    def linstor_delete_resource_all(res):
        cmd = 'linstor resource-definition delete %s' %res
        action = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = action.stdout
        if reg.judge_cmd_result_err(str(result)):
            print('Fail')
            # print('Cause:')
            # print(reg.get_err_mes(str(result)))
            print(result.decode('utf-8'))
        elif reg.judge_cmd_result_war(str(result)):
            print('Fail')
            print(result.decode('utf-8'))
        elif reg.judge_cmd_result_suc(str(result)):
            print('SUCCESS')
            return True

    #创建storagepool  -- ok
    @staticmethod
    def linstor_create_storagepool_lvm(node,stp,vg):
        cmd = 'linstor storage-pool create lvm %s %s %s' %(node,stp,vg)
        action = subprocess.run(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        result = action.stdout
        if reg.judge_cmd_result_err(str(result)):
            print('Fail')
            # print('Cause:')
            # print(reg.get_err_mes(str(result)))
            print(result.decode('utf-8'))
        elif reg.judge_cmd_result_suc(str(result)):
            print('SUCCESS')
            return True


    @staticmethod
    def linstor_create_storagepool_thinlv(node,stp,tlv):
        cmd = 'linstor storage-pool create lvmthin %s %s %s' %(node,stp,tlv)
        action = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = action.stdout
        if reg.judge_cmd_result_err(str(result)):
            print('Fail')
            # print('Cause:')
            # print(reg.get_err_mes(str(result)))
            print(result.decode('utf-8'))
        elif reg.judge_cmd_result_suc(str(result)):
            print('SUCCESS')
            return True


    #删除storagepool -- ok
    @staticmethod
    def linstor_delete_storagepool(node,stp):
        cmd = 'linstor storage-pool delete %s %s' %(node,stp)
        action = subprocess.run(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        result = action.stdout
        if reg.judge_cmd_result_err(str(result)):
            print('Fail')
            print(result.decode('utf-8'))
        elif reg.judge_cmd_result_war(str(result)):
            print('Fail')
            print(result.decode('utf-8'))
        elif reg.judge_cmd_result_suc(str(result)):
            print('SUCCESS')


    #创建集群节点
    @staticmethod
    def linstor_create_node(node,ip,nt):
        cmd = 'linstor node create %s %s  --node-type %s' %(node,ip,nt)
        nt_value = ['Combined','combined','Controller','Auxiliary','Satellite']
        if nt not in nt_value:
            print('node type error,choose from ''Combined','Controller','Auxiliary','Satellite''')
        else:
            action = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            result = action.stdout
            if reg.judge_cmd_result_err(str(result)):
                print('Fail')
                print(result.decode('utf-8'))
            elif reg.judge_cmd_result_war(str(result)):
                print('Fail')
                print(result.decode('utf-8'))
            elif reg.judge_cmd_result_suc(str(result)):
                print('SUCCESS')
                return True

    #删除node
    @staticmethod
    def linstor_delete_node(node):
        cmd = 'linstor node delete %s' %node
        action = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = action.stdout
        if reg.judge_cmd_result_err(str(result)):
            print('Fail')
            print(result.decode('utf-8'))
        elif reg.judge_cmd_result_war(str(result)):
            print('Fail')
            print(result.decode('utf-8'))
        elif reg.judge_cmd_result_suc(str(result)):
            print('SUCCESS')
            return True
        else:
            print(result.decode('utf-8'))

    #确认删除函数
    @staticmethod
    def confirm_del():
        print('Are you sure you want to delete it? If yes, enter \'y/yes\'')
        answer = input()
        if answer in ['y','yes']:
            return True
        else:
            return False



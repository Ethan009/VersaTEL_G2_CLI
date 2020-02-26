#coding:utf-8
import subprocess
import regex as reg

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
        #格式判断

        #执行
        action_c_rd = subprocess.run(cmd_rd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result_rd = action_c_rd.stdout

        #结果判断
        if reg.judge_cmd_result_suc(str(result_rd)):
            return True
        elif reg.judge_cmd_result_err(str(result_rd)):
            print('Fail')
            # print('Cause:')
            # print(reg.get_err_mes(str(result_rd)))
            print(result_rd.decode('utf-8'))
            return False

    @staticmethod
    def linstor_create_vd(res,size):
        cmd_vd = 'linstor vd c %s %s' % (res, size)
        action_c_vd = subprocess.run(cmd_vd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result_vd = action_c_vd.stdout

        if reg.judge_cmd_result_suc(str(result_vd)):
            return True
        elif reg.judge_cmd_result_err(str(result_vd)):
            LINSTOR_action.linstor_delete_rd(res)
            print('Fail')
            # print('Cause:')
            # print(reg.get_err_mes(str(result_vd)))
            print(result_vd.decode('utf-8'))
            return False


    #创建resource 自动
    @staticmethod
    def linstor_create_res_auto(res,size,num):
        cmd = 'linstor r c %s --auto-place %d' % (res, num)

        #格式判断
        # if not reg.judge_name(res):
        #     pass
        # else:
        #     print('')

        if LINSTOR_action.linstor_create_rd(res) and LINSTOR_action.linstor_create_vd(res,size):
            if reg.judge_num(str(num)):
                action = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                result = action.stdout
                if reg.judge_cmd_result_suc(str(result)):
                    print('SUCCESS')
                    return True
                elif reg.judge_cmd_result_err(str(result)):
                    LINSTOR_action.linstor_delete_rd(res)
                    print('Fail')
                    # print('Cause:')
                    # print(reg.get_err_mes(str(result)))
                    print(result.decode('utf-8'))



    #创建resource 手动
    @staticmethod
    def linstor_create_res_manual(res,size,node,stp):
        cmd = 'linstor resource create %s %s --storage-pool %s' %(node,res,stp)
        if LINSTOR_action.linstor_create_rd(res) and LINSTOR_action.linstor_create_vd(res,size):
            action = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            result = action.stdout
            if reg.judge_cmd_result_suc(str(result)):
                print('SUCCESS')
            elif reg.judge_cmd_result_err(str(result)):
                LINSTOR_action.linstor_delete_rd(res)
                print('Fail')
                # print('Cause:')
                # print(reg.get_err_mes(str(result)))
                print(result.decode('utf-8'))



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
        if reg.judge_cmd_result_suc(str(result)):
            print('SUCCESS')
        elif reg.judge_cmd_result_war(str(result)):
            print('Fail')
            # print('Cause:')
            # print(reg.get_cau_mes(str(result)))
            print(result.decode('utf-8'))


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
                # print('Cause:')
                # print(reg.get_err_mes(str(result)))
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
            # print('Cause:')
            # print(reg.get_err_mes(str(result)))
            print(result.decode('utf-8'))
        elif reg.judge_cmd_result_suc(str(result)):
            print('SUCCESS')
            return True


    #确认删除函数
    @staticmethod
    def confirm_del():
        print('Are you sure？y/n')
        answer = input()
        if answer in ['y','yes']:
            return True
        else:
            return False




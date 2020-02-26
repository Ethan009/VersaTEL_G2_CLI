#conding:utf-8
import re
import pprint

#for diskgroup

def judge_name(name):
    re_dg = re.compile('^[a-zA-Z][a-zA-Z0-9_-]*$')
    if re_dg.match(name):
        return name


def judge_size(size):
    re_size = re.compile('^[1-9][0-9.]*([KkMmGgTtPp]?(iB|B)?)$')
    if re_size.match(size):
        return size


def judge_num(num):
    re_num = re.compile('^[1-9][0-9]*')
    if re_num.match(num):
        return num



def judge_cmd_result_suc(cmd):
    re_suc = re.compile('SUCCESS')
    if re_suc.search(cmd):
        return True


def judge_cmd_result_err(cmd):
    re_err = re.compile('ERROR')
    if re_err.search(cmd):
        return True


def judge_cmd_result_war(cmd):
    re_err = re.compile('WARNING')
    if re_err.search(cmd):
        return True


def get_err_mes(cmd):
    re_mes_des = re.compile(r'(?<=Description:\\n)[\S\s]*(?=\\nCause:)')
    if re_mes_des.search(cmd):
        return (re_mes_des.search(cmd).group())


def get_cau_mes(cmd):
    re_mes_cau = re.compile(r'(?<=Cause:\\n)[\S\s]*(?=\\nDetails:)')
    if re_mes_cau.search(cmd):
        return re_mes_cau.search(cmd).group()

def get_err_mes_vd(cmd):
    re_mes_des = re.compile(r'(?<=Description:\\n)[\S\s]*(?=\\nDetails:)')
    if re_mes_des.search(cmd):
        return (re_mes_des.search(cmd).group())



# cmd = (b'\x1b[1;31mERROR:\n\x1b[0mDescription:\n    Node: nodea, Storage pool name: p'
#  b'ool_a already exists.\nCause:\n    The StorPool already exists\nDetails:\n  '
#  b'  Node: nodea, Storage pool name: pool_a\nShow reports:\n    linstor error'
#  b'-reports show 5E4CEC09-00000-000019\n')
#
#
#
# pprint.pprint(str(cmd))
#
# if get_cau_mes(str(cmd)):
#     print(get_cau_mes(str(cmd)))
# else:
#     print('创建失败')
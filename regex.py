#conding:utf-8
import re

#for diskgroup
def judge_name(name):
    re_dg = re.compile('^[a-zA-Z][a-zA-Z0-9_-]*$')
    if re_dg.match(name):
        return name


def judge_size(size):
    re_size = re.compile('^[1-9][0-9.]*([KkMmGgTtPpB](iB|B)?)$')
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


def get_err_not_vg(result,node,vg):
    re_ = re.compile(r'\(Node: \''+node+'\'\) Volume group \''+vg+'\' not found')
    if re_.search(result):
        return (re_.search(result).group())



def get_war_mes(result):
    re_ = re.compile(r'\x1b\[1;33mWARNING:\n\x1b(?:.*\s*)+\n$')
    if re_.search(result):
        return (re_.search(result).group())


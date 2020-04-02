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


def get_err_detailes(result):
    re_ = re.compile(r'Description:\n[\t\s]*(.*)\n')
    if re_.search(result):
        return (re_.search(result).group(1))

def get_war_mes(result):
    re_ = re.compile(r'\x1b\[1;33mWARNING:\n\x1b(?:.*\s*)+\n$')
    if re_.search(result):
        return (re_.search(result).group())



str_vg = ('  VG   #PV #LV #SN Attr   VSize VFree\n'
 '  vg1    1   3   0 wz--n- 2.38g 2.07g\n'
 '  vg2    1   1   0 wz--n- 2.38g 2.28g\n'
 '  vg3    1   1   0 wz--n- 2.38g 1.18g\n'
 '  vg4    1   0   0 wz--n- 2.84g 2.84g\n')

str_thinlv = ('  LV             VG   Attr       LSize   Pool Origin Data%  Meta%  Move Log '
 'Cpy%Sync Convert\n'
 '  res_a_00000    vg1  -wi-a----- '
 '104.00m                                                    \n'
 '  res_b_00000    vg1  -wi-a----- '
 '104.00m                                                    \n'
 '  res_test_00000 vg1  -wi-a----- '
 '104.00m                                                    \n'
 '  res_b_00000    vg2  -wi-a----- '
 '104.00m                                                    \n'
 '  lvol1          vg3  twi-a-tz--   1.19g             0.00   '
 '0.98                            \n')


def refining_thinlv(str):
    list = str.splitlines()
    list_thinlv = []
    re_ = re.compile(r'\s*(\S*)\s*(\S*)\s*\S*\s*(\S*)\s*\S*\s*\S*\s*\S*\s*?')
    for list_one in list:
        if 'twi' in list_one:
            thinlv_one = re_.findall(list_one)
            list_thinlv.append(thinlv_one[0])
    return list_thinlv

def refining_vg(str):
    list = str.splitlines()
    list_vg = []
    re_ = re.compile(r'\s*(\S*)\s*\S*\s*\S*\s*\S*\s*\S*\s*(\S*)\s*(\S*)\s*?')
    for list_one in list[1:]:
        vg_one = re_.findall(list_one)
        list_vg.append(vg_one[0])
    return list_vg


def get_option_lvm():
    vg = refining_vg(str_vg)
    thinlv = refining_thinlv(str_thinlv)
    list_vg = []
    list_thinlv = []
    for vg_one in vg:
        dict_vg = {"cityName":vg_one}
        list_vg.append(dict_vg)

    for thinlv_one in thinlv:
        dict_thinlv = {"cityName":thinlv_one}
        list_thinlv.append(dict_thinlv)

    dict_all = {"lvm":list_vg,"thin_lvm":list_thinlv}
    return dict_all



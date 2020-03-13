#coding:utf-8
import subprocess
import pprint

a = subprocess.getoutput('linstor --no-color --no-utf8 n l')
b = subprocess.getoutput('linstor --no-color --no-utf8 sp l')
c = subprocess.getoutput('linstor --no-color --no-utf8 r lv')
pprint.pprint(b)
pprint.pprint(c)
# -*- coding: utf-8 -*-
import re
import os
import shutil
# str="该网站多个子域名或页面存在虚假或恶意，虚假和恶意的内容会诱骗访问者上当或使您的计算机感染木马或病毒，此种情况可能是因为网站被黑客入侵篡改，为了避免给您造成损失，360安全中心已经帮您拦截，请您谨慎访问。"
# a=len(re.findall(u"虚假或恶意内容",str))
# print(a)
projectPath=os.getcwd()
try:
    if not os.path.exists(projectPath + '/data_copy'):
        os.makedirs(projectPath + '/data_copy')
    if not os.path.exists(projectPath + '/data_copy' + '/' + "20180725"):
        os.makedirs(projectPath + '/data_copy' + '/' + "20180725")
    if not os.path.exists(projectPath + '/data_copy' + '/' + "20180725" + '/' + "2018072508"):
        os.makedirs(projectPath + '/data_copy' + '/' + "20180725" + '/' + "2018072508")
    shutil.move("/data/qianhuhai/" + "20180725" + '/' + "2018072508" + '/' + "part-r-00",
                projectPath + '/data_copy' + '/' + "20180725" + '/' + "2018072508" + '/' + "part-r-00")
    os.remove("/data/qianhuhai/" + "20180725" + '/' + "2018072508" + '/' + "part-r-00")
except:
    print("error")

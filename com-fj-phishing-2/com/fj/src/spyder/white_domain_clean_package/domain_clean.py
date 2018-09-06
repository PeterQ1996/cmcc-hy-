# -*-coding:utf-8-*-
'''
过滤白名单
'''

import os,sys
import re
import traceback
from flashtext import KeywordProcessor

projectPath=os.getcwd()

class DomainClean():
    def __init__(self,param,whitePath):
        self.param=param
        self.whitePath=whitePath

    def cleanDomain(self):
        L = []
        black=[]
        keyword_processor=KeywordProcessor()

        f=open(self.whitePath,"r")
        for i in f.readlines():
            L.append(i.strip('\r\n'))

        keyword_processor.add_keywords_from_list(L)
        try:
            for i in self.param:  #待过滤的domain

                hostname, ip, ipBelong, firstVisitTime, lastestVisitTime, userSet, visitNum, similarityValue, imitate = \
                    i.strip('\r\n').split(";")

                hostname=hostname.strip('\r\n')

                try:
                    # if re.search("\."+j.strip('\r\n')+'$',hostname):
                    if len(keyword_processor.extract_keywords(hostname)) == 0:
                        black.append(i)
                except:
                    traceback.print_exc()


        except:
            traceback.print_exc()
            print("匹配错误")
        finally:
            f.close()
            return black


if __name__ == '__main__':
     whitePath=projectPath+"/white_list/white_list.txt"
     param = ["tk.haotibang.com;101.200.86.162:80;其他;0;1526426870510;1;18;0.5625;taobao.com"
         , "zs.ylzpay.com;202.101.157.200:8060;其他;0;1526426405595;1;4;0.61538464;alipay.com"
         , "zf.crv.com.cn;120.192.82.239:80;其他;0;1526427860332;1;5;0.61538464;cmbc.com.cn"
         , "tech.cpic.com.cn;117.131.74.128:80;其他;0;1526428690318;5;18;0.625;epicc.com.cn"
         , "www.100585.cn;47.90.53.47:80;其他;0;1526427560271;3;46;0.53846157;10086.cn"
         , "autohome.com.cn;47.90.53.47:80;其他;0;1526427560271;3;46;0.53846157;10086.cn"
         , "xs.autohome.com.cn;47.90.53.47:80;其他;0;1526427560271;3;46;0.53846157;10086.cn"
         , "xsx.xs.autohome.com.cn;47.90.53.47:80;其他;0;1526427560271;3;46;0.53846157;10086.cn"
         , "xsx.xs.takungpao.com;47.90.53.47:80;其他;0;1526427560271;3;46;0.53846157;10086.cn"
         , "takungpao.com;47.90.53.47:80;其他;0;1526427560271;3;46;0.53846157;10086.cn"
         , "tk.haotibang.com;101.200.86.162:80;其他;0;1526426870510;1;18;0.5625;taobao.com"]
     black=DomainClean(param,whitePath).cleanDomain()
     print(black)
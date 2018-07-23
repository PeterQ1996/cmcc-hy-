#!/usr/bin/env python
#-*-coding:utf-8-*-

import os,sys
from com.fj.src.spyder import AsynchronousCrawler
from com.fj.src.algorithm.model_predict import ModelRun
from com.fj.src.spyder.web_scan_probe import ContentGet_360
from com.fj.src.mysql_save_result import MySqlSave



#lujing
projectPath=os.getcwd()
sys.path.append(projectPath)



if __name__ == "__main__":

    # while(1):
    # dc=DomainConsumer("thread-1","1")
    try:
        g = open(projectPath + "/data/part-r-00000", 'r')  #输入待检测网站
    except:
        os.chdir(projectPath)
        g = open("data/part-r-00000", 'r')  # 输入待检测网站
    param = []
    for i in g.readlines():
        ki, vl = i.split('\t')

        param.append(vl.strip("\r\n"))

    # param=["tk.haotibang.com;101.200.86.162:80;其他;0;1526426870510;1;18;0.5625;taobao.com"
    # ,"zs.ylzpay.com;202.101.157.200:8060;其他;0;1526426405595;1;4;0.61538464;alipay.com"
    #    ,"zf.crv.com.cn;120.192.82.239:80;其他;0;1526427860332;1;5;0.61538464;cmbc.com.cn"
    #    ,"tech.cpic.com.cn;117.131.74.128:80;其他;0;1526428690318;5;18;0.625;epicc.com.cn"
    #    ,"www.100585.cn;47.90.53.47:80;其他;0;1526427560271;3;46;0.53846157;10086.cn"
    #    ]
    #

    ContentGet_360.ContentGet_360().run(param=param)
    # AsynchronousCrawler.AsynchronousCrawlerTxt().readUrl(domainInfo=param)
    g.close()


    MySqlSave.ConnectToSql()#存入数据库
    # ModelRun.modelrun()


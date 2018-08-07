#!/usr/bin/env python
# -*-coding:utf-8-*-


import traceback
import os, sys,shutil

projectPath = os.getcwd()  # lujing
sys.path.append(projectPath)

from com.fj.src.spyder import AsynchronousCrawler
from com.fj.src.algorithm.model_predict import ModelRun
from com.fj.src.spyder.web_scan_probe import ContentGet_360
from com.fj.src.spyder.web_scan_probe.selenium＿method import SeleniumMethod
from com.fj.src.mysql_save_result import MySqlSave
from com.fj.src.mysql_save_result import TextClean
from com.fj.src.spyder.white_domain_clean_package.domain_clean import DomainClean

if __name__ == "__main__":
    day = sys.argv[1]

    # while(1):
    # dc=DomainConsumer("thread-1","1")
    phantomJsPath = projectPath+"/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
    print(phantomJsPath)

    url360 = "http://webscan.360.cn/index/checkwebsite?url="
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
    proxy = 'http://www.xicidaili.com/wt'

    whitePath = projectPath + "/white_list/white_list.txt"
    for parent, dirnames, filenames in os.walk("/data/qianhuhai/" + day + '/'):
        for dirname in dirnames:
            print(dirname)
            rootPath = "/data/qianhuhai/" + day + '/' + dirname
            print(rootPath)

            for parent, dirnames, filenames in os.walk(rootPath):

                if len(filenames) == 0:
                    print("file为空")
                    break
                try:
                    for filename in filenames:

                        if not os.path.isfile("/data/qianhuhai/" + day + '/' + dirname + '/' + filename):
                            print("没有文件")

                            break
                        else:
                            g = open("/data/qianhuhai/" + day + '/' + dirname + '/' + filename, 'r')  # 输入待检测网站
                            print("/data/qianhuhai/" + day + '/' + dirname + '/' + filename)
                            print("有文件")
                            print(dirname)

                        param = []  #有新文件得清空存放域名的list
                        for i in g.readlines():
                            ki, vl = i.split('\t')
                            param.append(vl.strip("\r\n"))

                        black=DomainClean(param,whitePath).cleanDomain() #清洗一下


                        sm=SeleniumMethod(phantomJsPath,proxy,black,url360,user_agent)

                        sm.getIpList()

                        ContentGet_360.ContentGet_360().run(param=param)
                        # AsynchronousCrawler.AsynchronousCrawlerTxt().readUrl(domainInfo=param)

                        try:
                            g.close()
                        except:
                            print('wrong')
                        # MySqlSave.ConnectToSql()#存入数据库
                        # ModelRun.modelrun()

                        TextClean.TextClean()
                        if os.path.isfile(projectPath + "web_scan_probe/web-content"):
                            os.remove(projectPath + "/web_scan_probe/web-content")
                        try:
                            if not os.path.exists(projectPath + '/data_copy'):
                                os.makedirs(projectPath + '/data_copy')
                            if not os.path.exists(projectPath + '/data_copy' + '/'+day):
                                os.makedirs(projectPath + '/data_copy'+'/'+day )
                            if not os.path.exists(projectPath + '/data_copy' + '/'+day +'/'+dirname):
                                os.makedirs(projectPath + '/data_copy' + '/' + day +'/'+dirname)
                            shutil.move("/data/qianhuhai/" + day + '/' + dirname + '/' + filename,
                                        projectPath+'/data_copy'+'/'+ day +'/'+dirname +'/'+filename)

                        except:
                            print("移出文件出错!")
                except:
                    print("system error")

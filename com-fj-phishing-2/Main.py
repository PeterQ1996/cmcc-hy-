#!/usr/bin/env python
# -*-coding:utf-8-*-

import logging
import traceback
import os,sys,shutil

'''
项目路径
'''
projectPath = os.getcwd()
sys.path.append(projectPath)

'''
引用的包
'''
from com.fj.src.spyder import AsynchronousCrawler
from com.fj.src.algorithm.model_predict import ModelRun
from com.fj.src.spyder.web_scan_probe import ContentGet_360
from com.fj.src.spyder.web_scan_probe.selenium＿method import SeleniumMethod
from com.fj.src.mysql_save_result import MySqlSave
from com.fj.src.mysql_save_result import TextClean
from com.fj.src.spyder.white_domain_clean_package.domain_clean import DomainClean


'''
配置log
'''
logger=logging.getLogger("fishing detect")
file_handler=logging.FileHandler("fishinglog")
console_handler=logging.StreamHandler(sys.stdout)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.setLevel(logging.DEBUG)

'''
程序入口
'''
if __name__ == "__main__":
    # day = sys.argv[1]
    day = "20180725"
    phantomJsPath = projectPath+"/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
    url360 = "http://webscan.360.cn/index/checkwebsite?url="
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
    proxy = 'http://www.xicidaili.com/wt'
    whitePath = projectPath + "/white_list/white_list.txt"

    for parent, dirnames, filenames in os.walk("/data/qianhuhai/" + day + '/'):
        for dirname in dirnames:
            logger.debug(dirname) #2018072523
            rootPath = "/data/qianhuhai/" + day + '/' + dirname #/data/qianhuhai/20180725/2018072523
            logger.debug(rootPath)

            for parent, dirnames, filenames in os.walk(rootPath):

                if len(filenames) == 0:
                    logger.info("/data/qianhuhai/" + day + '/' + dirname+ ",目录下没有内容")  #  "/data/qianhuhai/" + day + '/' + dirname 目录下没有内容
                    break
                try:
                    for filename in filenames:

                        if not os.path.isfile("/data/qianhuhai/" + day + '/' + dirname + '/' + filename):
                            logger.debug("/data/qianhuhai/" + day + '/' + dirname+ ",目录下没有内容")
                            break
                        else:
                            g = open("/data/qianhuhai/" + day + '/' + dirname + '/' + filename, 'r')  # 输入待检测网站
                            logger.debug("/data/qianhuhai/" + day + '/' + dirname + '/' + filename)
                            logger.debug("/data/qianhuhai/" + day + '/' + dirname+ ",下有内容")


                        param = []  #有新文件得清空存放域名的list
                        for i in g.readlines():
                            ki, vl = i.split('\t')
                            param.append(vl.strip("\r\n"))

                        black=DomainClean(param,whitePath).cleanDomain() #清洗一下,


                        sm=SeleniumMethod(phantomJsPath,proxy,black,url360,user_agent) #360上验证

                        sm.getIpList()

                        ContentGet_360.ContentGet_360().run(param=black)
                        # AsynchronousCrawler.AsynchronousCrawlerTxt().readUrl(domainInfo=param)


                        g.close() #关闭文件

                        # MySqlSave.ConnectToSql()#存入数据库
                        # ModelRun.modelrun()

                        TextClean.TextClean() #清洗文件格式，从web-content到web-content-clean
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
                            os.remove("/data/qianhuhai/" + day + '/' + dirname + '/' + filename)
                        except:
                            logger.error("移出文件出错！")
                except:
                   logger.error("系统未知错误！")

# -*- coding: utf-8 -*-

from selenium import webdriver
import time
from urllib import request
import random
import os,sys
from selenium.webdriver.common.by import By
import socket
from selenium.webdriver.common.proxy import *
from bs4 import BeautifulSoup
import hashlib
import traceback

projectPath=os.getcwd()
sys.path.append(projectPath)

SEC=5
randomSEC=SEC+random.randint(0,9)/10 #sleep时间

class SeleniumMethod():

    def __init__(self,phantomJsPath,proxy,param,url360,user_agent):
        self.phantomJsPath=phantomJsPath
        self.proxy=proxy
        self.url360=url360
        self.user_agent=user_agent
        self.param=param
        self.l=[]
         # 获取相应的根目录
        if not os.path.exists(projectPath + '/web_scan_probe'):
            os.makedirs(projectPath + '/web_scan_probe')

        if not os.path.exists(projectPath + '/web_scan_probe/web_360_level'):
            os.makedirs(projectPath + '/web_scan_probe/web_360_level')

        if not os.path.exists(projectPath + '/web_scan_probe/web_chinaz_level'):
            os.makedirs(projectPath + '/web_scan_probe/web_chinaz_level')

    # def getProxyUrl(self):
    #     ip_list = []
    #     proxyRequest=request.Request(self.proxy)
    #     proxyRequest.add_header('User-agent',self.user_agent)
    #     proxyHtml=request.urlopen(proxyRequest).text
    #     soup=BeautifulSoup(proxyHtml,'lxml')
    #
    #     ul_list = soup.find_all('tr', limit=50)
    #     for i in range(2, len(ul_list)):
    #          line = ul_list[i].find_all('td')
    #          ip = line[1].text
    #          port = line[2].text
    #          address = ip + ':' + port
    #          ip_list.append(address)
    #
    #     return ip_list

    def getIpList(self):

        try:
            driver = webdriver.PhantomJS(executable_path= self.phantomJsPath)
            driver.set_window_size(1366, 768)

            for i in self.param:

                    hostname, ip, ipBelong, firstVisitTime, lastestVisitTime, userSet, visitNum, similarityValue, imitate = i.strip(
                        '\r\n').split(";")

                    print(hostname.strip('\r\n'))

                    hostname_encode = hostname.encode("unicode_escape")  # bytes
                    hmd = hashlib.md5()  #
                    hmd.update(hostname_encode)  # 生成文件的MD5值，MD5是一种哈希算法
                    md5_filename = hmd.hexdigest()

                    driver.get(self.url360+hostname)


            #inputs = driver.find_elements_by_id('webscan6').text

                    diaoyu_sec_360 = driver.find_element_by_xpath('//*[@id="diaoyu_sec"]')
                    print("diaoyu_sec:"+diaoyu_sec_360.text)

                    if diaoyu_sec_360.text == '有虚假或欺诈':
                        self.l.append([hostname, ip, ipBelong, firstVisitTime, lastestVisitTime, userSet, visitNum,
                                       similarityValue, imitate, md5_filename, diaoyu_sec_360])

                    with open(projectPath+"/log","a") as log:
                              log.write(hostname+diaoyu_sec_360.text+"\n")

                    time.sleep(randomSEC) #shuimianyixia
        except:
                traceback.print_exc()

        with open(projectPath + "/web_scan_probe/web-content", 'a') as L:
            for i in self.l:
                L.write(str(i).strip("[]") + '\n')
        return "scrapy end"


if __name__ == '__main__':
    phontomJsPath = projectPath + "/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"

    url360 = "http://webscan.360.cn/index/checkwebsite?url="
    url_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"

    proxy = 'http://www.xicidaili.com/wt'

    # param=["cc599.com;101.200.86.162:80;其他;0;1526426870510;1;18;0.5625;taobao.com"
    #                     ,"zs.ylzpay.com;202.101.157.200:8060;其他;0;1526426405595;1;4;0.61538464;alipay.com"
    #                        ,"zf.crv.com.cn;120.192.82.239:80;其他;0;1526427860332;1;5;0.61538464;cmbc.com.cn"
    #                        ,"tech.cpic.com.cn;117.131.74.128:80;其他;0;1526428690318;5;18;0.625;epicc.com.cn"
    #                        ]
    param=['07bbb.com;:80;其他;0;1532509056196;2;6;0.5555556;ccb.com', '1.bengne.com.cn;47.75.92.206:80;其他;0;1532509068879;2;2;0.53333336;cmbc.com.cn']
    sm=SeleniumMethod(phontomJsPath,proxy,param,url360,url_agent)
    listBack=sm.getIpList()
    print(listBack)

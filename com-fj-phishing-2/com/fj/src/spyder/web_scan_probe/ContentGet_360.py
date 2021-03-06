# -*- coding: utf-8 -*-
import os,sys
projectPath=os.getcwd()
sys.path.append(projectPath) #增加搜索路径
#白名单过滤的域名，会去３６０网站去验证其安全等级，
#非白名单的ｕｒｌ的也会下载其网站信息，并存储到路径projectPath下（工程的根目录）
#动态的内容也通过splash加载，
from urllib import request
import re
import time
import random
import hashlib
import traceback
import socket

import threading
import configparser
from com.fj.src.spyder.ContentGetHtml import ContentGetHtml
from lxml import etree
from io import StringIO



timeout = 5
socket.setdefaulttimeout(timeout)  #设置超时，　网页请求超时，则返回空，

cp=configparser.ConfigParser() #配置文件
projectPath=os.getcwd() #获得工程根目录
#-*-
cp.read('config.conf')#获取本机IP
IP=cp.get('localhost_ip','IP')
#-*-
#
# SEC=5
# randomSEC=SEC+random.randint(0,9)/10
# 解析３６０diaoyu_sec。判断是否是钓鱼网站
def parse_diaoyu_sec(param,conf):
    try:
       html=etree.HTML(param)
       if 1==conf:
          result=html.xpath('//*[@id="diaoyu_sec"]/text()')
          for i in result:

             return i

       elif conf==2:
           result=html.xpath('/html/body/div[2]/div[4]/div[3]/ul/li[2]/span[2]/text()')
           for i in result:
               return i
    except:
        traceback.print_exc()
#爬虫请求
def splashRun(detect_url):
    
    params_html = "&wait=0.5"  ###

    splash_url_html = "http://"+IP+":8050/render.html?"  ###
    oneUrlHtml = splash_url_html + detect_url + params_html  ###

    url_request = request.Request(oneUrlHtml)
    url_request.add_header('User-Agent',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    html = request.urlopen(url_request).read().decode("utf-8")  # str
    return html

class ContentGet_360(ContentGetHtml):

    def run(self, param ,param_day):

        # 获取相应的根目录
        if not os.path.exists(projectPath + '/web_scan_probe'):
            os.makedirs(projectPath + '/web_scan_probe')
        if not os.path.exists(projectPath + '/web_scan_probe/html'):
            os.makedirs(projectPath + '/web_scan_probe/html')
        if not os.path.exists(projectPath + '/web_scan_probe/png'):
            os.makedirs(projectPath + '/web_scan_probe/png')

        if not os.path.exists(projectPath + '/web_scan_probe/web_360_level'):
            os.makedirs(projectPath + '/web_scan_probe/web_360_level')

        if not os.path.exists(projectPath + '/web_scan_probe/web_chinaz_level'):
            os.makedirs(projectPath + '/web_scan_probe/web_chinaz_level')

        if not os.path.exists("/data/qianhuhai/png"):
            os.makedirs("/data/qianhuhai/png")
        if not os.path.exists("/data/qianhuhai/png/"+param_day):
            os.makedirs("/data/qianhuhai/png/"+param_day)

        for i in param:
            try:
                hostname, ip, ipBelong, firstVisitTime, lastestVisitTime, userSet, visitNum, similarityValue, imitate = i.strip(
                     '\r\n').split(";")


                detect_url = "url=http://" + hostname.strip('\n\r')  ###
                params_html = "&wait=0.5"  ###

                splash_url_html = "http://"+IP+":8050/render.html?"  ###
                oneUrlHtml = splash_url_html + detect_url + params_html  ###

                url_request = request.Request(oneUrlHtml)

                html1 = request.urlopen(url_request).read().decode("utf-8")  # str


                params_png = "&render_all=0&wait=0.5"  ### 加载时间等待2s
                splash_url_png = "http://"+IP+":8050/render.png?"  ###
                oneUrlPng = splash_url_png + detect_url + params_png  ###
                url_request = request.Request(oneUrlPng)  ###query下载图片
                png = request.urlopen(url_request).read()


                '''
                360验证结果
                '''
                # detect_url_360 = "url=http://" + "webscan.360.cn/index/checkwebsite?url=" + hostname.strip('\n\r')  ###
                # html2=splashRun(detect_url=detect_url_360)

                '''
                站长之家－金山毒霸
                '''
                #detect_url_chinaz = "url=http://"+"tool.chinaz.com/webscan/?host="+hostname.strip('\n\r')
                #html3=splashRun(detect_url=detect_url_chinaz)

                if html1 != '': #and html2 != '':  # 如果文本非空，才保存



                    # found_sensitive_words=keyword_processor.extract_keywords(returned_url_request_unicode)
                    # found_sensitive_words_len=len(found_sensitive_words)
                    hostname_encode = hostname.encode("unicode_escape")  # bytes
                    hmd = hashlib.md5()  #
                    hmd.update(hostname_encode)  # 生成文件的MD5值，MD5是一种哈希算法
                    md5_filename = hmd.hexdigest()  #
                    print(md5_filename)
                    if not os.path.isfile(projectPath+'/web_scan_probe/html'+'/'+md5_filename) :

                        with open(projectPath + "/web_scan_probe/html" + "/" + md5_filename,
                                  "w") as K:
                            K.write(html1)
                        if len(png) != '':
                            with open(projectPath + "/web_scan_probe/png" + "/" + md5_filename + ".png",
                                      "wb") as J:
                                J.write(png)

                            with open("/data/qianhuhai/png/" + param_day + '/' + md5_filename + ".png", "wb") as L:
                                L.write(png)

                        # with open(projectPath + '/web_scan_probe/web_360_level'+'/'+md5_filename,
                        #           'w') as f:
                        #     f.write(html2)


                       # with open(projectPath + '/web_scan_probe/web_chinaz_level'+'/'+md5_filename,
                       #           'w') as f:
                       #     f.write(html3)

                    '''
                    验证
                    '''
                    #diaoyu_sec_360 = parse_diaoyu_sec(html2, 1)  # 360验证结果

                    # diaoyu_sec_chinaz = parse_diaoyu_sec(html3, 2)  # chinaz验证结果
                    #if diaoyu_sec_360=='有虚假或欺诈':
                    #     self.l.append([hostname, ip, ipBelong, firstVisitTime, lastestVisitTime, userSet, visitNum,
                    #               similarityValue, imitate, md5_filename,diaoyu_sec_360])
                         
                    #with open(projectPath+"/log","a") as log:
                    #      log.write(hostname+firstVisitTime+diaoyu_sec_360+"\n")
                    # else:
                    #   if diaoyu_sec_chinaz=='危险':
                    #      self.l.append([hostname, ip, ipBelong, firstVisitTime, lastestVisitTime, userSet, visitNum,
                    #                    similarityValue, imitate, md5_filename, diaoyu_sec_chinaz])

                    #time.sleep(randomSEC)# 休眠５秒
                # if found_sensitive_words_len>1:
                #         self.result.append(1)
                # else:
                #         self.result.append(0)
                # for black_word in black_words:     ###
                #  word=black_word.strip('\n\r')###
                #  regex=unicode(word,"utf-8")###
                #  if  re.findall(regex,unicode(returned_url_request_unicode,"utf-8")) :###正则匹配的方法
                #      result.append(1)###
                #  result.append(0)###
            except:
                traceback.print_exc()

            # self.result.append(0)
        ###result=[0,1,0,1,...]  len(result)=len(self.url_list)
        # with open(projectPath + "/web_scan_probe/web-content", 'a') as L:
        #     for i in self.l:
        #         L.write(str(i).strip("[]") + '\n')
        return "scrapy end"


if __name__ == '__main__':

    flag = 0
    file_market = []

    if flag == 1:
        root1 = projectPath + "/web_scan_probe/png/"
        root2 = projectPath + "/web_scan_probe/logo/"
        if not os.path.exists(projectPath + "/web_scan_probe/png_dangers"):
            os.makedirs(projectPath + "/web_scan_probe/png_dangers")
    else:
        projectPath = "/home/qianhuhai/PycharmProjects/com-fj-phishing-2/"
        root1 = projectPath + "web_scan_probe/logo/"
        root2 = projectPath + "web_scan_probe/png/"
        if not os.path.exists(projectPath + "/web_scan_probe/png_dangers"):
            os.makedirs(projectPath + "/web_scan_probe/png_dangers")


    param = ["baidu.com;101.200.86.162:80;其他;0;1526426870510;1;18;0.5625;taobao.com",
        "tk.haotibang.com;101.200.86.162:80;其他;0;1526426870510;1;18;0.5625;taobao.com"
                         ,"zs.ylzpay.com;202.101.157.200:8060;其他;0;1526426405595;1;4;0.61538464;alipay.com"
                            ,"https://splash.readthedocs.io/en/stable/api.html;120.192.82.239:80;其他;0;1526427860332;1;5;0.61538464;cmbc.com.cn"
                            ,"tech.cpic.com.cn;117.131.74.128:80;其他;0;1526428690318;5;18;0.625;epicc.com.cn"
                            ,"www.100585.cn;47.90.53.47:80;其他;0;1526427560271;3;46;0.53846157;10086.cn"]

    ContentGet_360().run(param=param,param_day='20180725')

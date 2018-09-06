# -*-coding:utf-8-*-


import os
import time
import datetime
import traceback
from urllib import request
import requests
from lxml import etree


def TextClean():
    flag = 0
    projectPath = os.getcwd()
    f = open(projectPath + "/web_scan_probe/web-content", 'r')
    g = open(projectPath + "/web_scan_probe/web-content-clean", 'a')
    columns = len(list(f))
    f.close()
    f = open(projectPath + "/web_scan_probe/web-content", 'r')
    for i in f.readlines():
        try:
            flag = flag + 1
            hostname, ip, ipBelong, firstVisitTime, lastestVisitTime, userSet, visitNum, similarityValue, imitate, md5_filename, level \
                = i.strip('\r\n').split(',')

            userSet = userSet.strip(' ').replace("'", '')
            visitNum = visitNum.strip(' ').replace("'", '')
            hostname = hostname.strip(' ').replace("'", '')
            ip = ip.strip(' ').replace("'", '')


            imitate = imitate.strip(' ').replace("'", '')
            md5_filename = md5_filename.strip(' ').replace("'", '')
            lastestVisitTime = lastestVisitTime.strip(' ').replace("'", '')

            # strUserSet=int(userSet)
            # strVisitNum=int(visitNum)
            strHostName = hostname
            strIp = ip
            strImitate = imitate
            strMd5_Filename = 'png/' + md5_filename + '.png'
            lastestVisitTime = int(lastestVisitTime)
            lastestVisitTime = int(lastestVisitTime / 1000)

            found_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            time_local = time.localtime(lastestVisitTime)

            lastTime = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

            ipBelong = ipBelong.strip(' ').replace("'", '').encode('utf-8').decode('utf-8')

            ipBelong = ip_belongs(ip,ipBelong)


            record = strHostName + ',' + strIp + ',' + ipBelong + ',' + found_time + ',' + lastTime + ',' + userSet + ',' + visitNum + ',' + strImitate + ',' + \
                     strMd5_Filename + ',' + str(0)
            g.write(record + '\n')
        #  if flag!=columns:
        #    g.write(record+'\n')
        #  else:
        #    g.write(record)
        except:
            traceback.print_exc()
    f.close()
    g.close()


'''
处理ip归属地的函数 
'''


def ip_belongs(param_ip, param_ipBelong):
    ip, port = param_ip.split(':')
    url = r"http://www.ip138.com/ips138.asp?ip=" + ip + "&action=2"
    back_content = request.Request(url=url)

    back_content = requests.get(url).content

    # back_content_page=request.urlopen(back_content).read().decode('gbk')
    html = etree.HTML(back_content)

    xpath_content = html.xpath('/html/body/table/tr[3]/td/ul/li[1]/text()')

    if (param_ipBelong == '其他'):
        print(xpath_content[0].split('：')[1])
        param_ipBelong=param_ipBelong.replace('其他', xpath_content[0].split('：')[1]).strip()

    return param_ipBelong


if __name__ == '__main__':
    TextClean()
    a='其他'
    b='其他'
    if (a==b):
        print("is")


# -*-coding:utf-8-*-


import os
import time
import datetime
import traceback
def TextClean():
    flag=0
    projectPath = os.getcwd()
    f=open(projectPath+"/web_scan_probe/web-content",'r')
    g=open(projectPath+"/web_scan_probe/web-content-clean",'a')
    columns=len(list(f))
    f.close()
    f = open(projectPath + "/web_scan_probe/web-content", 'r')
    for i in f.readlines():
     try:
        flag=flag+1
        hostname, ip, ipBelong, firstVisitTime, lastestVisitTime, userSet, visitNum, similarityValue, imitate,md5_filename,level\
            =i.strip('\r\n').split(',')

        userSet=userSet.strip(' ').replace("'",'')
        visitNum = visitNum.strip(' ').replace("'", '')
        hostname = hostname.strip(' ').replace("'", '')
        ip = ip.strip(' ').replace("'", '')
        imitate=imitate.strip(' ').replace("'", '')
        md5_filename = md5_filename.strip(' ').replace("'", '')
        lastestVisitTime=lastestVisitTime.strip(' ').replace("'", '')

        # strUserSet=int(userSet)
        # strVisitNum=int(visitNum)
        strHostName=hostname
        strIp=ip
        strImitate=imitate
        strMd5_Filename= 'png/'+md5_filename +'.png'
        lastestVisitTime=int(lastestVisitTime)
        lastestVisitTime=int(lastestVisitTime/1000)

        found_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        time_local = time.localtime(lastestVisitTime)

        lastTime = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

        ipBelong=ipBelong.strip(' ').replace("'",'').encode('utf-8').decode('utf-8')


        record=strHostName+','+strIp+','+ipBelong+','+found_time+','+lastTime+','+userSet+','+visitNum+','+ strImitate+','+\
                    strMd5_Filename +','+str(0)
        g.write(record+'\n')
      #  if flag!=columns:
      #    g.write(record+'\n')
      #  else:
      #    g.write(record)
     except:
        traceback.print_exc()
    f.close()
    g.close()

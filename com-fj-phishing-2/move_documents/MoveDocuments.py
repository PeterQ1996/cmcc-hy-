#-*-coding=utf-8-*-

import  os,sys
import shutil
sys.path.append('/home/qianhuhai/PycharmProjects/com-fj-phishing-2')


def mv(srcfile,dstfile):
     if not os.path.isfile(srcfile):
         print('%s not exists' %(srcfile))
     else:
         fpath,fname=os.path.split(dstfile)
         if not os.path.exists(fpath):
             os.mkdir(fpath)
         shutil.copyfile(srcfile,dstfile)
         print('%s -> %s' %(srcfile,dstfile))


with open('../data/file_list_03.txt','r') as f:
    for i in f.readlines():
        label,url,file=i.strip('\r\n').split(',')
        for j in ['/home/qianhuhai/PycharmProjects/com-fj-phishing-2/file_02',
                  '/home/qianhuhai/PycharmProjects/com-fj-phishing-2/web_scan_probe/html']:
           srcfile=j+'/'+file
           dstfile='/home/qianhuhai/PycharmProjects/com-fj-phishing-2/file_01'+'/'+file
           mv(srcfile,dstfile)
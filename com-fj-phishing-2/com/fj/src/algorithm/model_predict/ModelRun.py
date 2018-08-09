# _*_ coding=utf-8 _*_

import os,sys
projectPath=os.getcwd()
sys.path.append(projectPath)
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
import traceback
from com.fj.src.algorithm.model_predict import DataQingXi
from com.fj.src.algorithm.model_predict import GetLabel1data, DataExtract


corpus=[]
label=[]
def modelrun():
  DataQingXi.dataQingXi()  #调用DataQingXi
  DataExtract.dataExtract() #DataExtract
  with open(projectPath+'/data/vocabulary.txt','r')  as f:
      a = f.read()
      vocabulary = eval(a)


  g=open(projectPath+"/data/unknowndata03.txt","r")
  for cc in g.readlines():
       corpus.append(cc.strip('\r\n'))

  vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,vocabulary=vocabulary)
  tfidf= vectorizer.fit_transform(corpus)

  train_X = tfidf

  try:
       with open(projectPath+"/model/clf.pkl",'rb') as h:
           clf=pickle.load(h)

       predicted = clf.predict(train_X)

       GetLabel1data.getlabel1(predicted)
  except :
    traceback.print_exc()




if __name__ == '__main__':
    # param=['07bbb.com;:80;其他;0;1532509056196;2;6;0.5555556;ccb.com', '1.bengne.com.cn;47.75.92.206:80;其他;0;1532509068879;2;2;0.53333336;cmbc.com.cn',
    #        'cc599.com;:80;其他;0;1532509056196;2;6;0.5555556;ccb.com', "tk.haotibang.com;101.200.86.162:80;其他;0;1526426870510;1;18;0.5625;taobao.com"
    #         , "zs.ylzpay.com;202.101.157.200:8060;其他;0;1526426405595;1;4;0.61538464;alipay.com"
    #         , "zf.crv.com.cn;120.192.82.239:80;其他;0;1526427860332;1;5;0.61538464;cmbc.com.cn"
    #         , "tech.cpic.com.cn;117.131.74.128:80;其他;0;1526428690318;5;18;0.625;epicc.com.cn"
    #         , "www.100585.cn;47.90.53.47:80;其他;0;1526427560271;3;46;0.53846157;10086.cn"]


    modelrun()
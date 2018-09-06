# -*- coding: utf-8 -*-

##主要是解决图像相似度匹配的问题
#pip install opencv_python
##图像相似度问题
##调用了opencv2
import cv2
import scipy as sp
import os,sys
import shutil
import traceback

projectPath=os.getcwd() #获取根目录径径

def sift(path1,path2):
    '''
    sift图像相似度
    :param path1:
    :param path2:
    :return:
    '''

    img1 = cv2.imread(path1, 0)


    img2 = cv2.imread(path2, 0)

    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    print('matches...', len(matches))
    # Apply ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)
    print('good', len(good))
    # #####################################
    # visualization
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    view = sp.zeros((max(h1, h2), w1 + w2, 3), sp.uint8)
    view[:h1, :w1, 0] = img1
    view[:h2, w1:, 0] = img2
    view[:, :, 1] = view[:, :, 0]
    view[:, :, 2] = view[:, :, 0]

    for m in good:
        # draw the keypoints
        # print m.queryIdx, m.trainIdx, m.distance
        color = tuple([sp.random.randint(0, 255) for _ in range(3)])
        # print 'kp1,kp2',kp1,kp2
        cv2.line(view, (int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1])),
                 (int(kp2[m.trainIdx].pt[0] + w1), int(kp2[m.trainIdx].pt[1])), color)

    cv2.imshow("view", view)
    cv2.waitKey(20)
    return len(good)


if __name__=="__main__":
    flag=0
    file_market=[]

    if flag==1:
      root1=projectPath+"/web_scan_probe/png/"
      root2=projectPath+"/web_scan_probe/logo/"
      if not os.path.exists(projectPath+"/web_scan_probe/png_dangers"):
          os.makedirs(projectPath+"/web_scan_probe/png_dangers")
    else:
      projectPath="/home/qianhuhai/PycharmProjects/com-fj-phishing-2/"
      root1 = projectPath + "web_scan_probe/logo/"
      root2 = projectPath + "web_scan_probe/png/"
      if not os.path.exists(projectPath+"/web_scan_probe/png_dangers"):
          os.makedirs(projectPath+"/web_scan_probe/png_dangers")
    for Root,Path,Files in os.walk(root1):
        for File in Files:
            path1=os.path.join(root1,File)
            print(path1)
            for root,path,files in os.walk(root2):
                for file in files:
                   path2=os.path.join(root2,file)
                   try:
                     if File=='cgb.png':
                      if sift(path1,path2)>30:
                       file_market.append(file)
                       shutil.move(root2+file,projectPath+"web_scan_probe/png_dangers")

                   except:

                       traceback.print_exc()


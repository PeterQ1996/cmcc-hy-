# -*- coding: utf-8 -*-

import hashlib



if __name__ == '__main__':
    param=['codc.com.cn','cdsac.cn','cdsa.org']
    for i in param:
        hostname_encode = i.strip('\r\n').encode("unicode_escape")  # bytes
        hmd = hashlib.md5()  #
        hmd.update(hostname_encode)  # 生成文件的MD5值，MD5是一种哈希算法
        md5_filename = hmd.hexdigest()
        print(md5_filename)
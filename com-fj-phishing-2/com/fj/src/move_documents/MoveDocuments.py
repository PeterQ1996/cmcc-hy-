# -*-coding=utf-8-*-

import os, sys
import shutil

projectPath = os.getcwd()
sys.path.append(projectPath)


def mv(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print('%s not exists' % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)
        if not os.path.exists(fpath):
            os.mkdir(fpath)
        shutil.copyfile(srcfile, dstfile)
        print('%s -> %s' % (srcfile, dstfile))


#!/usr/bin/python2
# -*- coding: utf-8 -*-
# @Author  : huyabing

import sys,os,json,commands,hashlib
from xml.etree import ElementTree as ET


reload(sys)
sys.setdefaultencoding('utf8')


def write_txt(argv):
    tmp = {}
    md5file = 'AssetMD5Verify.txt'
    p_dirname = "version/%s/AssetBundles/%s/%s" %(argv[1],argv[1],argv[2])
    dir_name = "%s/%s" %(p_dirname,argv[3])
    filesname = dir_name.split('/')[-1]
    zipname = "%s.zip" %(filesname)
    tmp = {"ZipFileName":zipname,"Infos":[]}
    os.chdir(dir_name)
    del_xml(argv[2])
    for root, dirs, files in os.walk('./'):
      for name in files:
         filepath = os.path.join(root, name)
         filename = filepath[2:]
         extension = os.path.splitext(filepath)[1]
         mainfile = '%s/%s.manifest' %(argv[2],argv[2])
         delfile = '%s_Versions.xml' %(argv[2])
         if extension == ".manifest" and filename != mainfile:
            continue
         if extension != ".unity3d" or "script/" in filename:
            md5,size = get_md5(filepath)
            ret = {"FileName":filename,"MD5":md5,"Size":size}
            tmp["Infos"].append(ret)
    file(md5file,'wb').write(json.dumps(tmp))
    print filesname +' AssetMD5Verify.txt Ok'


def del_xml(name):
    xml_name="%s_Versions.xml" %(name)
    cmd="find ./ -name %s -delete" %(xml_name)
    commands.getoutput(cmd)


def get_md5(filename):
    size = os.path.getsize(filename)
    myhash = hashlib.md5()
    f = file(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
           break
        myhash.update(b)
    f.close()
    md5 = myhash.hexdigest()
    return md5,size

if __name__ == '__main__':
    if len(sys.argv) != 4 :
      print '''-- make_md5sum.py --\nparam1: version dir name,  e.g. Alpha\nparam2: plat name,  e.g. iOS\nparam3: versionname,  e.g. 90421_90433\nUSAGE EXAMPLE: ./make_md5sum.py Alpha iOS 90421_90433'''
      sys.exit(2)
    write_txt(sys.argv)

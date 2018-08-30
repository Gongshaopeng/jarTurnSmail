# -*- coding: utf-8 -*-
# @Time    : 2018/8/29 下午5:36
# @Author  : Gongshaopeng
# @File    : JarTSmailManage.py
# @Software: PyCharm
import os
import time
import urllib
import requests

# smail工具包下载地址可根据自己的需求下载baksmali包： https://bitbucket.org/JesusFreke/smali/downloads/

toolbaksmaliUrl = "https://bitbucket.org/JesusFreke/smali/downloads/baksmali-2.1.3.jar"
toolbaksmali = "baksmali-2.1.3.jar"

#获取文件路径
path = (os.path.dirname(os.path.abspath(__file__)))

# 自定义文件名
dexFileName = "build";
jarFileName = "channel"
samilFileName = "smail"
toolsFileName = "tools"


# 文件路径
buildFile = path + "/" + dexFileName
channelFile = path + "/" + jarFileName
smailFile = path + "/" + samilFileName
toolsFile = path + "/" + toolsFileName

# 创建文件分类管理目录

def createFile():
    isFile(buildFile, dexFileName)
    isFile(channelFile, jarFileName)
    isFile(smailFile, samilFileName)
    isFile(toolsFile, toolsFileName)


def cmdAnd(smailCmd):
     os.popen(smailCmd)

def isFile(path,name):
    folder0 = os.path.exists(path)
    if not folder0:  # 判断文件是否存在
        os.makedirs(path)
        time.sleep(3)
        print(name + "不存在")
    else:
        print(name + "存在")


def cmdSmail(samilFileName,dexPath,dexName):
    smailCmd = "java -jar " + path + "/"+toolsFileName+"/" + toolbaksmali + " -o " +  samilFileName + " " + dexPath
    cmdAnd(smailCmd)
    print(dexName + "smail转译中")
    time.sleep(3)
    print(dexName + "smail转译完成")

def cmdDex(dexPath,jarFileName,jar,dexName):
    dexcmd = path + "/"+toolsFileName+"/dx --dex --output=" + dexPath +" "+ path + "/" + jarFileName + "/" + jar
    cmdAnd(dexcmd)
    print(dexName + "dex文件生成中")
    time.sleep(3)

def down(_save_path, _url):
    folder4 = os.path.exists(_save_path)
    if not folder4:  # 判断dex是否存在
        print(toolbaksmali + "不存在")
        r = requests.get(_url)
        with open(_save_path, "wb") as code:
            code.write(r.content)
        print(toolbaksmali + "下载完成")
    else:
        print(toolbaksmali + "存在")


class JarManager(object):

    def getJarList(self,file_dir):
        result = []
        for root, dirs, files in os.walk(file_dir):
            result = files  # 当前路径下所有非目录子文件
        return result

    def excuteJar2Dex(self,path,jars):

        for jar in jars:

            fileName = str(jar.split('.jar')[0:][0])
            dexName = fileName +".dex"
            dexPath = buildFile+"/" + dexName
            channelPath = channelFile+ "/" + jar
            newFilePath = smailFile + "/" + fileName

            folder0 = os.path.exists(channelPath)

            if not folder0:  # 判断Jar是否存在
                print(jar + "不存在")
            else:
                print(jar + "存在")
                folder1 = os.path.exists(dexPath)
                if not folder1:  # 判断dex是否存在
                    cmdDex(dexPath,jarFileName,jar,dexName);
                else:
                    print(dexName + "存在")

            print(dexName + "dex文件转译完成")
            # 创建新文件夹
            isFile(newFilePath,fileName)

            folder2 = os.path.exists(dexPath)
            if not folder2:  # 判断dex是否存在
                print(dexName + "不存在")

            else:
                print(dexName + "存在")
                fileSize = newFilePath + "/com"
                folder3 = os.path.exists(fileSize)
                if not folder3:  # 判断Samil转译文件夹是否存为空
                    print(fileName + "文件为空")
                    cmdSmail(newFilePath, dexPath, dexName)
                else:
                    print(fileName + "文件存在")




if __name__ == "__main__":
    createFile();
    down(toolsFile+"/"+toolbaksmali,toolbaksmaliUrl)
    jarManager = JarManager()
    jarNameList = jarManager.getJarList(path+"/channel/")
    jarManager.excuteJar2Dex(path,jarNameList)
    print("结束了")
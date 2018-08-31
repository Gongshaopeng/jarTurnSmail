#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/29 下午5:36
# @Author  : Gongshaopeng
# @File    : JarTSmailManage.py
# @Software: PyCharm
import os
import time
import shutil
# import requests

#获取dx 工具
#
# mac下 dx 工具获取
#
#/Users/Roger/Library/Android/sdk/build-tools/xxxxx(这里是工具的版本号，例如：28.0.2)/dx
#
#Git 获取地址：https://github.com/Gongshaopeng/jarTurnSmail.git


# smail工具包官网下载地址，可根据自己的需求下载baksmali包： https://bitbucket.org/JesusFreke/smali/downloads/

toolbaksmaliUrl = "https://bitbucket.org/JesusFreke/smali/downloads/baksmali-2.1.3.jar"
toolbaksmali = "baksmali-2.1.3.jar" #这里的工具名字一定要与下载名一致

#获取文件路径
path = (os.path.dirname(os.path.abspath(__file__)))

# 自定义文件名
dexFileName = "build";
jarFileName = "channel"
samilFileName = "smail"
toolsFileName = "tools"
logFileName = "log"
errorFNS  = "errorSmail.txt"
errorFND  = "errorDex.txt"
successFN  = "success.txt"

# 文件路径
buildFile = path + "/" + dexFileName
channelFile = path + "/" + jarFileName
smailFile = path + "/" + samilFileName
toolsFile = path + "/" + toolsFileName
logFile = path + "/" + logFileName
errorFileS = path + "/"+logFileName+"/" + errorFNS
errorFileD = path + "/"+logFileName+"/" + errorFND
successFile = path +"/"+logFileName+ "/" + successFN

# 原工具路径
dxpath = path + "/dx"
dxjarpath = path + "/dx.jar"
baksmalipath = path + "/" + toolbaksmali

# 执行时工具路径

dxRpath = toolsFile + "/dx"
dxjarRpath = toolsFile + "/dx.jar"
baksmaliRpath = toolsFile + "/" + toolbaksmali

#下载目标的全路径
dowFilePath = path+"/"+toolbaksmali


#下载文件到指定目录
# def down(_save_path, _url):
#     addfileName = os.path.basename(_save_path) #获取文件名
#     folder4 = os.path.exists(_save_path)
#     if not folder4:  # 判断dex是否存在
#         print(addfileName + "不存在")
#         r = requests.get(_url)
#         with open(_save_path, "wb") as code:
#             code.write(r.content)
#         print(addfileName + "下载完成")
#
#     else:
#         print(addfileName + "存在")


def isConfiguration(cpath,rpath):
    #先检测tools文件夹里是不是空的
    folder6 = os.path.exists(cpath)
    addfileName = os.path.basename(cpath)  # 获取文件名
    if not folder6:  # 判断文件是否存在,如果是空的再去检查外部根目录
        folder5 = os.path.exists(rpath)
        addfileName = os.path.basename(rpath)  # 获取文件名
        if not folder5:  # 判断文件是否存在
            print("检测到" + addfileName + "文件不存在，注意添加" + addfileName + "否则脚本运行不起来")
        else:
            print("检测到" + addfileName + "文件在外部，移动到"+toolsFileName+"文件下")
            fileMove(rpath);
    else:
        print("检测到" + addfileName + "文件存在")



# 移动文件
def fileMove(renamePath):
    shutil.move(renamePath, toolsFile)


# 创建文件分类管理目录
def createFile():
    #创建管理目录
    isFile(buildFile, dexFileName)
    isFile(channelFile, jarFileName)
    isFile(smailFile, samilFileName)
    isFile(toolsFile, toolsFileName)
    # down(dowFilePath,toolbaksmaliUrl)

    isFile(logFile, logFileName)
    # isFile(errorFile, errorFN)
    # isFile(successFile, successFN)

    #验证工具包和移动工具包
    isConfiguration(dxRpath,dxpath);
    isConfiguration(dxjarRpath,dxjarpath);
    isConfiguration(baksmaliRpath,baksmalipath);


# 执行命令
def cmdAnd(smailCmd):
     os.popen(smailCmd)

# 创建文件夹
def isFile(path,name):
    folder0 = os.path.exists(path)
    if not folder0:  # 判断文件是否存在
        print("检测到"+name + "文件夹不存在")
        os.makedirs(path)
        time.sleep(3)
        print("文件夹"+name + "创建成功")

    else:
        print("文件夹"+name + "存在")



# dex 转译 smail
def cmdSmail(samilFileName,dexPath,dexName):
    try:
        smailCmd = "java -jar " + baksmaliRpath + " -o " + samilFileName + " " + dexPath
        errorSmailCode = cmdAnd(smailCmd)
        print(dexName + "smail转译中")
    except  errorSmailCode:
        print("Error:文件名" + dexName + errorSmailCode)
        logWriteTxt(errorFileS, dexName + errorSmailCode);
    else:
        time.sleep(3)
        print(dexName + "smail转译完成")


# jar 转译 dex
def cmdDex(dexPath,jarFileName,jar,dexName):
        dexcmd = dxRpath + " --dex --output=" + dexPath + " " + path + "/" + jarFileName + "/" + jar
        cmdAnd(dexcmd)
        print(dexName + "dex文件生成中")
        time.sleep(3)
        print(dexName + "Dex转译完成")


# 记录错误日志
def logWriteTxt(textPath,text):

    with open(textPath, 'a') as file:
        write_str = text + " \n"
        file.write(write_str)

# 逻辑管理类
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
                print(jar + "存在，开始验证dex")
                folder1 = os.path.exists(dexPath)
                if not folder1:  # 判断dex是否存在
                    try:
                        errorDexCode = cmdDex(dexPath, jarFileName, jar, fileName);
                    except  errorDexCode:
                        print("Error:文件名" + fileName + errorDexCode)
                        logWriteTxt(errorFileS, fileName + errorDexCode);

                else:
                    print(dexName + "存在")

            # 创建Smail管理目录
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
                    try:
                      errorSmailCode = cmdSmail(newFilePath, dexPath, fileName)
                    except  errorSmailCode :
                        print("Error:文件名" + fileName + errorSmailCode)
                        logWriteTxt(errorFileS, fileName + errorSmailCode);
                else:
                    print(fileName + "文件存在")




if __name__ == "__main__":
    createFile();
    jarManager = JarManager()
    jarNameList = jarManager.getJarList(path+"/channel/")
    jarManager.excuteJar2Dex(path,jarNameList)
    print("结束了")
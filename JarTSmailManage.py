#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/29 下午5:36
# @Author  : Gongshaopeng
# @File    : JarTSmailManage.py
# @Software: PyCharm
import os
import time
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


# 创建文件分类管理目录
def createFile():
    #创建管理目录
    isFile(buildFile, dexFileName)
    isFile(channelFile, jarFileName)
    isFile(smailFile, samilFileName)

    # isFile(toolsFile, toolsFileName)
    # down(dowFilePath,toolbaksmaliUrl)

    isFile(logFile, logFileName)
    # isFile(errorFile, errorFN)
    # isFile(successFile, successFN)

# 执行命令
def cmdAnd(smailCmd):
     os.popen(smailCmd)

# 创建文件夹
def isFile(path,name):
    folder0 = os.path.exists(path)
    if not folder0:  # 判断文件是否存在
        print("检测到文件夹"+name + "不存在")
        os.makedirs(path)
        time.sleep(3)
        print("文件夹"+name + "创建成功")

    else:
        print("文件夹"+name + "存在")


# dex 转译 smail
def cmdSmail(samilFileName,dexPath,dexName):
    try:
        smailCmd = "java -jar " + path + "/" + toolbaksmali + " -o " + samilFileName + " " + dexPath
        cmdAnd(smailCmd)
        print(dexName + "smail转译中")
    except Exception as err:
        print("Error:文件名" + dexName +str(err))
        logWriteTxt(errorFileS, dexName +str(err));
    else:
        time.sleep(3)
        print(dexName + "smail转译完成")


# jar 转译 dex
def cmdDex(dexPath,jarFileName,jar,dexName):
        dexcmd = path + "/dx --dex --output=" + dexPath + " " + path + "/" + jarFileName + "/" + jar
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
                        cmdDex(dexPath, jarFileName, jar, fileName);
                    except Exception as err:
                        print("Error:文件名" + fileName + str(err))
                        logWriteTxt(errorFileD, fileName + str(err));

                else:
                    print(dexName + "存在")

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
                    try:
                        cmdSmail(newFilePath, dexPath, fileName)
                    except Exception as err:
                        print("Error:文件名" + fileName + err)
                        logWriteTxt(errorFileS, fileName + err);
                else:
                    print(fileName + "文件存在")




if __name__ == "__main__":
    createFile();
    jarManager = JarManager()
    jarNameList = jarManager.getJarList(path+"/channel/")
    jarManager.excuteJar2Dex(path,jarNameList)
    print("结束了")
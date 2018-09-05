#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/29 下午5:36
# @Author  : Gongshaopeng
# @File    : JarTSmailManage.py
# @Software: PyCharm
import os
import time
import shutil
# import commands
# import subprocess
from subprocess import Popen, PIPE

# import requests

# 获取dx 工具
#
# mac下 dx 工具获取
#
# /Users/Roger/Library/Android/sdk/build-tools/xxxxx(这里是工具的版本号，例如：28.0.2)/dx
#
# Git 获取地址：https://github.com/Gongshaopeng/jarTurnSmail.git


# smail工具包官网下载地址，可根据自己的需求下载baksmali包： https://bitbucket.org/JesusFreke/smali/downloads/

toolbaksmaliUrl = "https://bitbucket.org/JesusFreke/smali/downloads/baksmali-2.1.3.jar"
toolbaksmali = "baksmali-2.1.3.jar"  # 这里的工具名字一定要与下载名一致

# 获取文件路径
path = (os.path.dirname(os.path.abspath(__file__)))

# =================================================================================================

# 自定义文件名
dexFileName = "build"
jarFileName = "channel"
samilFileName = "smail"
toolsFileName = "tools"
logFileName = "log"

# 状态日志
errorFNS = "errorSmail.txt"
errorFND = "errorDex.txt"
successFNS = "successSmail.txt"
successFND = "successDex.txt"
# =================================================================================================

# 文件路径
buildFile = path + "/" + dexFileName
channelFile = path + "/" + jarFileName
smailFile = path + "/" + samilFileName
toolsFile = path + "/" + toolsFileName
logFile = path + "/" + logFileName
errorFileS = logFile + "/" + errorFNS
errorFileD = logFile + "/" + errorFND
successFileS = logFile + "/" + successFNS
successFileD = logFile + "/" + successFND

# =================================================================================================

# 原工具路径（同Python文件的根目录下）
dxpath = path + "/dx"
dxjarpath = path + "/dx.jar"
baksmalipath = path + "/" + toolbaksmali

# 执行时工具路径 （工具管理文件夹下 toolsFile）
dxRpath = toolsFile + "/dx"
dxjarRpath = toolsFile + "/dx.jar"
baksmaliRpath = toolsFile + "/" + toolbaksmali

# 下载目标的全路径
dowFilePath = path + "/" + toolbaksmali

# =================================================================================================
# isFile(logFile, logFileName)
# isFile(errorFile, errorFN)
# isFile(successFile, successFN)
# 初始化文件管理目录
listFile = [[buildFile, dexFileName], [channelFile, jarFileName], [smailFile, samilFileName],
            [toolsFile, toolsFileName],[logFile, logFileName]]
# 配置工具文件移动路径
listConfig = [[dxRpath, dxpath], [dxjarRpath, dxjarpath], [baksmaliRpath, baksmalipath]]


# =================================================================================================


# 下载文件到指定目录
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


# 检测配置文件是否缺少
def isConfiguration(cpath, rpath):
    # 先检测tools文件夹里是不是空的
    folder6 = os.path.exists(cpath)
    addfileName = os.path.basename(cpath)  # 获取文件名
    if not folder6:  # 判断文件是否存在,如果是空的再去检查外部根目录
        folder5 = os.path.exists(rpath)
        addfileName = os.path.basename(rpath)  # 获取文件名
        if not folder5:  # 判断文件是否存在
            print("检测到" + addfileName + "文件不存在，请注意添加" + addfileName + "否则脚本无法正常编译")
        else:
            print("检测到" + addfileName + "文件在外部，移动到" + toolsFileName + "文件下")
            fileMove(rpath)
    else:
        print("检测到" + addfileName + "文件存在")


# 移动文件
def fileMove(renamePath):
    shutil.move(renamePath, toolsFile)


# 删除文件
def removeFile(my_file):
    fname = os.path.basename(my_file)  # 获取文件名
    if os.path.exists(my_file):
        # 删除文件，可使用以下两种方法。
        os.remove(my_file)
        # os.unlink(my_file)
        print(fname + "日志已删除")
    else:
        print("未发现" + fname + "日志")


# 创建文件夹
def isFile(path, name):
    folder0 = os.path.exists(path)
    if not folder0:  # 判断文件是否存在
        print("检测到" + name + "文件夹不存在,开始创建")
        os.makedirs(path)
        time.sleep(3)
        print("文件夹" + name + "创建成功")
    else:
        print("文件夹" + name + "存在")


# 遍历文件计算大小，等于 0 的都是空目录
def getFileSize(filePath, size=0):
    for root, dirs, files in os.walk(filePath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
            # print(f)
    return size


# 创建文件分类管理目录
def createFile():
    print("==============检测配置以及环境==============")

    # 创建管理目录
    for fileItme in listFile:
        isFile(fileItme[0], fileItme[1])

        # 验证工具包和移动工具包
    for runCpath in listConfig:
        isConfiguration(runCpath[0], runCpath[1])

    # 下载baksmali工具包
    # down(dowFilePath,toolbaksmaliUrl)

    # print("——重置工具日志——")
    # removeFile(errorFileD)
    # removeFile(errorFileS)
    # removeFile(successFileD)
    # removeFile(successFileS)

    print("==============配置环境检测结束==============")

# 执行命令
def cmdAnd(smailCmd):
   p = Popen(smailCmd, shell=True, stdout=PIPE, stderr=PIPE)
   p.wait()
   return p
   # if p.returncode != 0:
   #     return -1
   # else:
   #     return 0

# dex 转译 smail
def cmdSmail(samilFileName, dexPath, dexName):
    smailCmd = "java -jar " + baksmaliRpath + " -o " + samilFileName + " " + dexPath
    print(dexName + ".smail转译中")
    p = Popen(smailCmd, shell=True, stdout=PIPE, stderr=PIPE)
    p.wait()
    # p = cmdAnd(smailCmd)
    stdout,stderr = p.communicate()
    if p.returncode == 0:
        message = "Success:转译成功 " + dexName + ".smail "
        out = stdout.decode('utf-8')
        logWriteTxt(successFileS, message +"\n"+ str(out))
        print(dexName + ".smail转译完成")
    else:
        message = "Error:转译.Smail失败_ " + dexName + " 文件"
        print(message)
        err = stderr.decode('utf-8')
        errStr = ""
        if errStr == "":
           errStr ="AbnormalStart:\n"+str(err)+"\nAbnormalEnd"
        logWriteTxt(errorFileS, message +"\n"+ errStr)

    time.sleep(3)



# jar 转译 dex
def cmdDex(dexPath, jarFile, jar, dexName):
    dexcmd = dxRpath + " --dex --output=" + dexPath + " " + path + "/" + jarFile + "/" + jar
    # p = cmdAnd(dexcmd)
    p = Popen(dexcmd, shell=True, stdout=PIPE, stderr=PIPE)
    p.wait()
    stdout,stderr = p.communicate()
    print(dexName + ".dex文件生成中" + dexPath)
    if p.returncode == 0:
        message = "Success:转译成功 " + dexName + ".dex "
        out = stdout.decode('utf-8')
        logWriteTxt(successFileD, message+"\n"+str(out))
        print(dexName + ".dex转译完成" + str(out))
    else:
        message = "Error:转译.dex失败_文件名： " + dexName + " "
        err = stderr.decode('utf-8')
        print(message+str(err))
        errStr = ""
        if errStr == "":
            errStr = "AbnormalStart:\n" + str(err) + "\nAbnormalEnd"
        logWriteTxt(errorFileD, message+"\n"+errStr)


    time.sleep(3)



# 记录错误日志
def logWriteTxt(textPath, text):
    with open(textPath, 'a') as file:
        write_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "  " + text + " \n"
        file.write(write_str)


# 逻辑管理类
class JarManager(object):

    def getJarList(self, file_dir):
        result = []
        for root, dirs, files in os.walk(file_dir):
            result = files  # 当前路径下所有非目录子文件
        return result

    def excuteJar2Dex(self, path, jars):

        for jar in jars:
            suffixName = os.path.splitext(jar)[-1] #获取文件名
            if suffixName == ".jar":
                print(jar+"文件后缀是.jar,开始编译")
                fileName = str(jar.split('.jar')[0:][0])
                dexName = fileName + ".dex"
                dexPath = buildFile + "/" + dexName
                channelPath = channelFile + "/" + jar
                newFilePath = smailFile + "/" + fileName

                folder0 = os.path.exists(channelPath)
                if not folder0:  # 判断Jar是否存在
                    print(jar + "不存在")
                else:
                    print(jar + "存在，开始验证dex")
                    folder1 = os.path.exists(dexPath)
                    if not folder1:  # 判断dex是否存在
                        print(dexName + "不存在,开始转换")
                        cmdDex(dexPath, jarFileName, jar, fileName)
                    else:
                        print(dexName + "已存在,跳过转换")



                folder2 = os.path.exists(dexPath)
                if not folder2:  # 判断dex是否存在
                    print(dexName + "不存在,.smail转换停止")

                else:
                    # 创建Smail管理目录
                    isFile(newFilePath, fileName)
                    print(dexName + "存在,开始转换.smail")
                    # fileSize = newFilePath + "/com"
                    # print("文件大小 %f",getFileSize(newFilePath))
                    # folder3 = os.path.getsize(newFilePath)
                    if getFileSize(newFilePath) == 0:  # 判断Samil转译文件夹是否存为空
                        print(fileName + "文件内容为空,转换.smail")

                        cmdSmail(newFilePath, dexPath, fileName)
                    else:
                        print(fileName + ".smail,已转换过")

            else:
                print(jar+ "文件后缀不是.jar,跳过此文件")


if __name__ == "__main__":
    createFile()
    jarManager = JarManager()
    jarNameList = jarManager.getJarList(path + "/channel/")
    jarManager.excuteJar2Dex(path, jarNameList)
    print("==============结束了==============")



# 获取 后缀名(扩展名) / 文件名
# file = "Hello.py"
#
# # 获取前缀（文件名称）
# assert os.path.splitext(file)[0] == "Hello"
#
# # 获取后缀（文件类型）
# assert os.path.splitext(file)[-1] == ".py"
# assert os.path.splitext(file)[-1][1:] == "py"

# 反编译工具之—批量jar转译Smail

#### 前言：
  由于本次的工作需求是批量jar反编译为smail，也就小小的研究了一下android反编译，用Python写了一个自动化反编译脚本，此脚本支持终端直接使用。python源码中还附写了爬取工具包到本地指定目录的方法，在python 支持库环境的编译器中使用可把download代码打开，可自动下载。

#### jar转smali文件逻辑： 
    
    先将jar文件转为.dex文件，
    再将.dex文件转为smali文件
    jar ——> dex ——> smail 




#### 安装教程

+ 配置python脚本运行的环境
![python脚本配置环境.png](https://upload-images.jianshu.io/upload_images/6884657-b60abbbb155da98f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
注：图中的 baksmail 、dx、dx.jar 必需与python放在同一目录下

1.查找dx工具位置（下图来自于Mac 环境）
```
/Users/Roger/Library/Android/sdk/build-tools/xxxxx(这里是工具的版本号，例如：28.0.2)/dx
```
![dx工具位置.png](https://upload-images.jianshu.io/upload_images/6884657-99babe3ad3a373d9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


2. baksmail.jar工具包下载地址
smail工具包官网下载地址，可根据自己的需求下载baksmali包：
 https://bitbucket.org/JesusFreke/smali/downloads/

+ dx 工具使用方法
1.使用dx可执行脚本方式
dx --dex --output=(转化后文件名，可自定义).dex (包名).jar 
2.直接使用dx.jar工具库方式
java -jar dx.jar --dex --output=(转化后文件名).dex (包名).class
+ 将dex文件转来smali文件
使用baksmali.jar库
java -jar baksmali.jar (之前定义的文件名).dex


#### 使用说明

+ python脚本的使用方法：
![管理目录说明.png](https://upload-images.jianshu.io/upload_images/6884657-661595ebe50b7386.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1.如果脚本存在的文件夹中没有管理目录，那么先运行一下脚本，会自动生成。
2.把要转译的.jar包文件，放入channel文件夹中
3.运行工具，可选择支持 python 的编译器（我使用的是pyCharm）,终端也可直接使用

注：终端运行python文件的使用方法
  1.  cd 到文件夹目录
  2.  在文件首行添加#!/usr/bin/env python （已添加）
  3.  添加权限 chmod 777 (文件名).py
  4.  执行脚本./(文件名).py

终端第一次运行结果如图：

![A2C361F0-B330-477F-B804-F182C53A445B.png](https://upload-images.jianshu.io/upload_images/6884657-5cfae4922f3d6d53.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![管理目录说明.png](https://upload-images.jianshu.io/upload_images/6884657-daa380f8af16be8c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

终端测试效果图：

![62A2F7B1-7912-42DC-B3E7-1AE475E58D90.png](https://upload-images.jianshu.io/upload_images/6884657-7096c7d1cf3f90f8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注意查看文件：
![6F0838BC-37E6-422D-915A-ED2FB1669014.png](https://upload-images.jianshu.io/upload_images/6884657-60a56de0d7802353.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![9CE5A80C-9405-4D6E-A72E-7787592EEB90.png](https://upload-images.jianshu.io/upload_images/6884657-e06467852d337acc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![746DA9AE-0C2B-4A76-9821-B177307C2A38.png](https://upload-images.jianshu.io/upload_images/6884657-5ad79c83a4002b21.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

核心代码：

```
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

# 执行命令
def cmdAnd(smailCmd):
   p = Popen(smailCmd, shell=True, stdout=PIPE, stderr=PIPE)
   p.wait()
   if p.returncode != 0:
       return -1
   else:
       return 0

   # dex 转译 smail
def cmdSmail(samilFileName, dexPath, dexName):
    smailCmd = "java -jar " + baksmaliRpath + " -o " + samilFileName + " " + dexPath
    print(dexName + ".smail转译中")
    p = cmdAnd(smailCmd)
    if p == 0:
        message = "Success:转译成功 " + dexName + ".smail "
        logWriteTxt(successFileS, message)
        print(dexName + ".smail转译完成")
    else:
        message = "Error:转译.Smail失败_ " + dexName + " 文件"
        print(message)
        logWriteTxt(errorFileS, message);

    time.sleep(3)



# jar 转译 dex
def cmdDex(dexPath, jarFile, jar, dexName):
    dexcmd = dxRpath + " --dex --output=" + dexPath + " " + path + "/" + jarFile + "/" + jar
    p = cmdAnd(dexcmd)
    print(dexName + ".dex文件生成中" + dexPath)
    if p == 0:
        message = "Success:转译成功 " + dexName + ".dex "
        logWriteTxt(successFileD, message)
        print(dexName + ".dex转译完成")
    else:
        message = "Error:转译.dex失败_失败文件名： " + dexName + " "
        print(message)
        logWriteTxt(errorFileD, message);


    time.sleep(3)



# 记录错误日志
def logWriteTxt(textPath, text):
    with open(textPath, 'a') as file:
        write_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "  " + text + " \n"
        file.write(write_str)
        

```

####总结：
此次用到了Python语法中的文件管理，认识了对本地文件的操作：增、删、改、查。了解了Python的命令操作，以及线程安全，熟悉了在python环境下如何使用命令，以及存在的线程堵塞处理。尝试了python网络爬取文件，下载处理，以及下载到指定文件目录操作。




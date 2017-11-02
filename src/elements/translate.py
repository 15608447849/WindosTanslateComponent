#coding:utf-8
import threading
import win32com,win32com.client
import os,subprocess,re,os.path,platform,sys
from datetime import datetime, timedelta
import tkinter
import tkinter.messagebox
import pythoncom
import configparser
from socket import *
import time

#保存 监听路径 , 轮询时间
class TranslateObjcet():
    def __init__(self):
        self.obLock = threading.Lock() #互斥锁 acquire() - release()
        self.isInit = False


    #初始化参数
    def initValue(self,ffmpeg,moniterPath,moniterTime):
        if self.isInit :
            return
        self.dirc = self.repleceFileSeparator(moniterPath)
        self.sec = int(moniterTime)
        self.ffmpeg = ffmpeg
        if not os.path.exists(self.ffmpeg):
            tkinter.messagebox.showerror('错误', '找不到ffmpeg.exe文件!')
            sys.exit(-1)

        # print(self.dirc,self.sec)
        self.regexVideo = "Video: (.*?), (.*?), (.*?)[,\\s]"
        self.regexAudio = "Audio: (\\w*), (\\d*) Hz"
        self.regexVok = "\.vok"
        self.regexVideoSuffix = "\.(?:avi|rm|rmvb|mpeg|mpg|mpg|dat|mov|oq|asf|wmv|mp4)"
        self.regexWordSuffix = "\.(?:doc|docx)"
        self.regexWorkbookSuffix = "\.(?:xls|xlsl)"
        self.regexPptSuffix = "\.(?:ppt|pptx)"
        self.regexDuration = "Duration: (.*?), start: (.*?), bitrate: (\\d*) kb\\/s"

        self.regex_video = re.compile(self.regexVideo, re.IGNORECASE)
        self.regex_audio = re.compile(self.regexAudio, re.IGNORECASE)
        self.regex_file = re.compile(self.regexVok, re.IGNORECASE)
        self.regex_VideoSuffix = re.compile(self.regexVideoSuffix, re.IGNORECASE)
        self.regex_WordSuffix = re.compile(self.regexWordSuffix, re.IGNORECASE)
        self.regex_WorkbookSuffix = re.compile(self.regexWorkbookSuffix, re.IGNORECASE)
        self.regex_PptSuffix = re.compile(self.regexPptSuffix, re.IGNORECASE)
        self.regex_Duration = re.compile(self.regexDuration, re.IGNORECASE)
        self.isInit = True
    # 替换路径
    def repleceFileSeparator(self, path):
        return re.compile('\\\\').sub('/', path)

    # 查询文件夹下所有内容并执行检测
    def eachDirctoryAndCheck(self):
        # print("开始遍历主目录...",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        if(self.obLock.acquire()):
            try:
                for root, dirs, files in os.walk(self.dirc):
                    # print(root, dirs, files)
                    try:
                        for file in files:
                            # print( os.path.basename(file))
                            self.word2pdf(root, file)
                            self.xlsx2pdf(root, file)
                            self.ppt2pdf(root, file)
                            self.videoTrans(root, file)
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
            self.obLock.release()

    #word -> pdf
    def word2pdf(self, sourceDir, sourceFile):
        try:
            fileSuffix = result = re.findall(r'\.[^.\\/:*?"<>|\r\n]+$', sourceFile)
            if fileSuffix.__len__() == 0:
                return

            strarr = self.regex_WordSuffix.findall(fileSuffix[0])
            if strarr.__len__() == 0:
                return

            # 判断是否存在PDF
            path = self.repleceFileSeparator(sourceDir + '/' + sourceFile)
            if os.path.exists(path + '.pdf'):
                return

            pythoncom.CoInitialize()
            wps = None
            try:
                wps = win32com.client.Dispatch('KWPS.Application')
                wps.Visible = 0
                wps.DisplayAlerts = 0
                doc = wps.Documents.Open(path)
                doc.SaveAs(path + '.pdf', 17)
                wps.Documents.Close(path)
                wps.Quit()
                wps = None
                print("转换成功: " + path + '.pdf')
            except Exception as e:
                print(e)
            finally:
                try:
                    wps.Quit()
                except Exception as e:
                    pass
        except Exception as e:
                    print(e)

    #xlsx->pdf
    def xlsx2pdf(self,sourceDir,sourceFile):
        try:
            fileSuffix = result = re.findall(r'\.[^.\\/:*?"<>|\r\n]+$', sourceFile)
            if fileSuffix.__len__() == 0:
                return
            strarr = self.regex_WorkbookSuffix.findall(fileSuffix[0])
            if strarr.__len__() == 0:
                return
            # 判断是否存在PDF
            path = self.repleceFileSeparator(sourceDir + '/' + sourceFile)
            if os.path.exists(path + '.pdf'):
                return

            pythoncom.CoInitialize()
            excel = None
            try:
                excel = win32com.client.Dispatch('KET.Application.9')
                excel.Visible = 0
                excel.DisplayAlerts = 0
                workbook = excel.Workbooks.Open(path)
                workbook.ExportAsFixedFormat(0, path + ".pdf")
                workbook.Close(path)
                # wps.Documents.Close(wps.wdDoNotSaveChanges)
                excel.Quit()
                excel = None
                print("转换成功: " + path + '.pdf')
            except Exception as e:
                print(e)
            finally:
                try:
                    excel.Quit()
                except Exception as e:
                    pass
        except Exception as e:
            print(e)

    def ppt2pdf(self,sourceDir, sourceFile):
        try:
            fileSuffix = result = re.findall(r'\.[^.\\/:*?"<>|\r\n]+$', sourceFile)
            if fileSuffix.__len__() == 0:
                return
            strarr = self.regex_PptSuffix.findall(fileSuffix[0])
            if strarr.__len__() == 0:
                return
            # 判断是否存在PDF
            path =  self.repleceFileSeparator(sourceDir + '/' + sourceFile)
            if os.path.exists(path + '.pdf'):
                return

            pythoncom.CoInitialize()
            wpp = None
            try:
                wpp = win32com.client.Dispatch('Kwpp.Application')
                # wpp.Visible = 0
                # wpp.DisplayAlerts = 0
                ppt = wpp.Presentations.Open(path)
                ppt.SaveAs(path + '.pdf', 32)
                ppt.Close()
                wpp.Quit()
                wpp = None
                print("转换成功: " + path + '.pdf')
            except Exception as e:
                print(e)
            finally:
                try:
                    wpp.Quit()
                except Exception as e:
                    pass
        except Exception as e:
            print(e)

    def videoTrans(self, sourceDir,sourceFile):
        try:
            strarr = self.regex_VideoSuffix.findall(sourceFile)
            if strarr.__len__() == 0:
                return
            strarr = self.regex_file.findall(sourceFile)
            if strarr.__len__() > 0:
                return

            path = self.repleceFileSeparator(sourceDir + '/' + sourceFile)
            if os.path.exists(path + '.vok'):
                return
            self.videoTransImps(path)
        except Exception as e:
            print(e)

    def videoTransImps(self, path):
        temp = path + '.trs'
        cur_path = '"' + path + '"'

        command_info = self.ffmpeg + ' -i ' + cur_path
        output = subprocess.getoutput(command_info)
        stringArr_video = self.regex_video.findall(output)
        stringArr_audio = self.regex_audio.findall(output)

        if stringArr_video.__len__() == 0 or stringArr_audio.__len__() == 0 or stringArr_video[0][0] == 'h264' and \
                        stringArr_audio[0][0] == 'aac':
            self.createFile(path + '.vok')
            return

        temp_path = '"' + temp + '"'
        command_execute = self.ffmpeg + ' -y -copyts -threads 4 -i ' + cur_path + ' -f mp4 -coder 1 -vcodec libx264 -strict experimental -acodec aac -crf 24 -subq 5 -g 250 -qmin 10 -qmax 51 -qcomp 0.60 -ab 128k -ar 44100 -ac 2 ' + temp_path
        output = subprocess.getoutput(command_execute)
        # os.remove(path)
        # print('删除源文件')
        os.rename(path, path + ".vok")
        os.rename(temp, path)
        print('转换成功 : ' + path)
        # +'\n'+output

    #创建文件
    def createFile(self, path):
        f = None
        try:
            f = open(path, 'w')
            f.close()
            f = None
        except Exception as e:
            print(e)
        finally:
            if not f is None:
                f.close()

    def getVideoLengthAndTranslate(self,path):
        resp = 'node'
        try:
            path = self.repleceFileSeparator(path)
            if os.path.exists(path + '.vok'):
                os.remove(path + '.vok')  # 删除.vok文件
            # videoTransImps(path)
            command = "ffmpeg.exe -i " + '"' + path + '"'
            output = subprocess.getoutput(command)
            # print(output)
            arr = self.regex_Duration.findall(output)
            if arr.__len__() > 0:
                threading.Thread(target=self.videoTransImps, args=(path,)).start() #另起一个线程转换
                resp = arr[0][0]
        except Exception as e:
            print(e)
        return resp

    #开始执行
    def execute(self):
        self.tag = True
        self.loop(func=self.eachDirctoryAndCheck,second=self.sec)

    #轮询任务
    def loop(self, func,day=0, hour=0, min=0, second=0):
        # Init time
        while self.tag:
            now = datetime.now()
            strnow = now.strftime('%Y-%m-%d %H:%M:%S')
            # print("当前时间:", strnow)

            period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
            next_time = now + period
            strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
            # print("下一次时间:", strnext_time)

            while self.tag and str(strnow) != str(strnext_time):
                now = datetime.now()
                strnow = now.strftime('%Y-%m-%d %H:%M:%S')

            if self.tag:
                # print("执行监听.")
                func()
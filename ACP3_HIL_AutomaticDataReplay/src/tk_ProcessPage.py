import tkinter as tk
from tkinter import ttk
from ExternalCall_CANoe import *
from ExternalCall_INCA import *
import tkinter as tk
from pandas import read_csv
from can import BLFReader
import os,sys
import time
import threading
import pythoncom

class ProcessPage:
    def __init__(self,master:tk.Tk,Start_File,Replay_File,Folderpath,pattern) -> None:
        self.root=master
        self.root.title("台架自动化回灌录制")
        self.root.geometry("900x620")
        self.Start_File=Start_File
        self.Replay_File=Replay_File
        self.Folderpath=Folderpath
        self.pattern=pattern  
        
        self.ProcessNum=0
        self.AlreadyProNum=tk.IntVar()
        self.AlreadyProNum.set(self.ProcessNum)
        self.AllProNum=tk.IntVar()
        self.FileLists=[]
        self.bg_color='snow'
        self.fg_color="red"
        self.Pause_flag=0
        if self.pattern==2:
            self.ListDir=os.listdir(self.Folderpath)
            self.result_path=Folderpath+"/Result"
            if not os.path.isdir(self.result_path):
                os.mkdir(self.result_path)  
            #Filter asc & blf file
            for i in self.ListDir:
                format=i.split(".")[-1]
                if(format=="blf" or format=="asc"):
                    self.FileLists.append(i)
            self.NumberOfFile=len(self.FileLists)
        else:
            self.result_path='/'.join(self.Replay_File.split("/")[:-1])
            self.NumberOfFile=1
            self.FileLists.append(self.Replay_File.split("/")[-1])
        
        self.text1=tk.StringVar()
        self.text1.set("需要处理的文件数: "+str(self.NumberOfFile))
        self.text2=tk.StringVar()
        self.text2.set("剩余要处理的文件数:  "+str(self.NumberOfFile-self.ProcessNum))
             
        self.root.configure(background=self.bg_color)
        self.root=tk.Frame(self.root,bg=self.bg_color)
        self.root.pack()
        
        self.row7=tk.Frame(self.root,bd =1 ,relief = tk.SUNKEN,bg=self.bg_color)
        self.row7.pack(side = tk.BOTTOM,fill="x")
        self.row7.configure(background=self.bg_color)
        tk.Label(self.row7, text='保存位置 >>> '+self.result_path, anchor =tk.W, bg=self.bg_color, font="Calibri 11 bold").pack(side = tk.LEFT) 
        tk.Label(self.row7, text='|版权所属:ADAS标定开发股', anchor =tk.W, bg=self.bg_color, font="Calibri 10 bold").pack(side = tk.RIGHT)        
        
        self.row1=tk.Frame(self.root)
        self.row1.pack()
        self.row1.configure(background=self.bg_color) 
        tk.Label(self.row1, textvariable=self.text1, font="Calibri 15 bold", bg=self.bg_color, fg="red").pack(padx=0,fill='y')
        
        self.row2=tk.Frame(self.root)
        self.row2.pack(pady=7)
        self.row2.configure(background=self.bg_color) 
        tk.Label(self.row2, textvariable=self.text2, font="Calibri 15 bold", bg=self.bg_color, fg="red").pack(padx=0,fill='y')

        self.row21=tk.Frame(self.root,bd =1 ,relief = tk.SUNKEN)
        self.row21.pack(fill="x")
        self.row21.configure(background=self.bg_color) 
        tk.Label(self.row21,text='程序运行状态', width=72,borderwidth=2,relief="ridge",bg=self.bg_color, font="Calibri 11 bold").pack(side=tk.LEFT)
        tk.Label(self.row21,text='剩余文件列表', width=32,borderwidth=2,relief="ridge",bg=self.bg_color, font="Calibri 11 bold").pack(side=tk.LEFT)
        
        self.row3=tk.Frame(self.root)
        self.row3.pack(expand=tk.YES, fill=tk.BOTH)
        self.row3.configure(background=self.bg_color)
        scrollbar = tk.Scrollbar(self.row3, bg=self.bg_color)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.list_box = tk.Listbox(self.row3, width=27,height=22,selectmode="multiple", font="Arial 11", bg=self.bg_color)
        self.list_box.pack(side="right",expand=tk.YES, fill="both")
        self.list_box.config(yscrollcommand=scrollbar.set)
        scrollbarx =tk.Scrollbar(self.list_box, orient=tk.HORIZONTAL)
        scrollbarx.pack(side=tk.BOTTOM, fill=tk.BOTH)
        scrollbar.config(command=self.list_box.yview)
        scrollbarx.config(command=self.list_box.xview)
        
        scrollbar2 = tk.Scrollbar(self.row3, bg=self.bg_color)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.BOTH)       
        self.list_box2 = tk.Listbox(self.row3, width=70,height=22,selectmode="multiple", font="Arial 11", bg=self.bg_color)
        self.list_box2.pack(expand=tk.YES, fill="both")
        self.list_box2.config(yscrollcommand=scrollbar2.set)
        scrollbarx2 =tk.Scrollbar(self.row3, orient=tk.HORIZONTAL)
        scrollbarx2.pack(side=tk.BOTTOM, fill=tk.BOTH)
        scrollbar2.config(command=self.list_box2.yview)
        scrollbarx2.config(command=self.list_box2.xview)
        
        self.row4=tk.Frame(self.root)
        self.row4.pack(expand=tk.YES, fill=tk.BOTH,pady=7)
        self.row4.configure(background=self.bg_color)
        tk.Label(self.row4, text='当前文件回灌进度', anchor =tk.W, bg=self.bg_color, font="Calibri 11 bold").pack(side = tk.LEFT) 
        self.Progress=ttk.Progressbar(self.row4,length=700)
        self.Progress.pack(side = tk.LEFT,padx=7)
        
      
        self.row5=tk.Frame(self.root)
        self.row5.pack(expand=tk.YES, fill=tk.BOTH,pady=7)
        self.row5.configure(background=self.bg_color)
        tk.Button(self.row5, text='退出', command=self.exit,width=8).pack(side = tk.RIGHT,padx=10)
        self.Pause=tk.Button(self.row5, text='暂停', command=self.replayPause,width=8)
        self.Pause.pack(side = tk.RIGHT,padx=10)
        self.Continue=tk.Button(self.row5, text='继续', command=self.replayContinue,width=8)
        self.Continue.pack(side = tk.RIGHT,padx=10)
        self.Continue.config(state=tk.DISABLED)
        
        # show FileList Info by list_box
        for i in self.FileLists:
            self.list_box.insert("end",i)             
        
        self.list_box2.insert("end","开始回灌")
          
        self._Start()
    
    def _showProgress(self,t):
        p=threading.Thread(target=self.showProgress,args=(t,)) 
        p.setDaemon(True)  
        p.start()
    
    def showProgress(self,t):
        self.Progress['maximum']=10*t
        self.Progress['value']=0
        for i in range(10*t):
            self.Progress['value']+=1
            self.root.update()
            time.sleep(0.1)
    
    def replayContinue(self):
        if (self.NumberOfFile-self.ProcessNum)==0:
            self.list_box2.insert("end","所有文件已回灌完成！！")
            self.Continue.config(state=tk.DISABLED)
            return         
        self.Continue.config(state=tk.DISABLED)
        self.Pause.config(state=tk.ACTIVE)
        self.Pause_flag=0
        self.list_box2.insert("end","继续开始回灌")  
        self._Start()
        
    def replayPause(self):
        if (self.NumberOfFile-self.ProcessNum)==0:
            self.list_box2.insert("end","所有文件已回灌完成！！")
            self.Pause.config(state=tk.DISABLED)
            return  
        self.Pause.config(state=tk.DISABLED)
        self.Pause_flag=1
        self.list_box2.insert("end","播放完当前文件将暂停...")  
                
    def _Start(self):
        p=threading.Thread(target=self.Start) 
        p.setDaemon(True)  
        p.start()

    def Start(self):      
        pythoncom.CoInitialize()
        #Canoe init
        self.app_Caone = CANoe()
        self.app_Caone.stop_Measurement()
        #INCA init
        self.INCA=Inca()
        self.INCA.get_openExp()
        self.INCA.stop_record()
        self.INCA.stop_measurement()
        self.INCA.set_record_path(self.result_path)
        self.INCA.start_measurement()
        if self.pattern==2:  
            # Batch File Load
            FileListsCopy=self.FileLists
            for File in FileListsCopy:
                format=File.split(".")[-1]
                # get file time
                if format=='asc':
                    framefile = read_csv(self.Folderpath+"/"+File,skiprows=4,encoding="gbk",
                                        engine='python',sep=' ',delimiter=None, index_col=False,header=None,skipinitialspace=True)
                    file_time=framefile.values[-3][0]
                    t=int(float(file_time))
                else :          #format=='blf'
                    log_data = BLFReader(self.Folderpath+"/"+File)
                    file_start=log_data.start_timestamp
                    file_end=log_data.stop_timestamp
                    t=int(float(file_end)-float(file_start)) 
                    
                self.list_box2.insert("end","------------------------------------------------------------------") 
                self.list_box2.insert("end",File+" 将播放"+str(t)+"s")
                self.list_box2.insert("end",File+" 加载中...")      
                self.list_box2.see(tk.END)                   
                # set file
                self.app_Caone.set_ReplayBlock_File(self.Folderpath+"/"+File)
                self.INCA.set_record_filename(File)     
                # start 
                self.app_Caone.start_Measurement()           
                self.INCA.start_record()
                if t<30:
                    self._showProgress(t)
                else:
                    self._showProgress(int(0.94*t))
                self.list_box2.insert("end",File+" 回放并记录中...")
                self.list_box2.see(tk.END) 
                time.sleep(t) #wait data replay finish
                self.INCA.stop_record()
                self.app_Caone.stop_Measurement()  
                
                self.ProcessNum+=1
                self.list_box2.insert("end",File+" 完成回放并保存...")
                self.list_box2.insert("end","------------------------------------------------------------------")
                self.list_box2.see(tk.END)   
                self.list_box.delete(0)
                self.FileLists=self.FileLists[1:]
                self.text2.set("剩余要处理的文件数:  "+str(self.NumberOfFile-self.ProcessNum))    
                if self.Pause_flag==1: 
                    self.Continue.config(state=tk.ACTIVE)
                    self.list_box2.insert("end"," 回灌已暂停...")      
                    self.list_box2.see(tk.END)
                    break 
            
            if self.ProcessNum==self.NumberOfFile:
                self.list_box2.insert("end","------------------------------------------------------------------")
                self.list_box2.insert("end","所有数据已回灌完成！！！")
                self.Pause.config(state=tk.DISABLED)
                self.Continue.config(state=tk.DISABLED)
                self.list_box2.see(tk.END)
                        
        else: #pattern==1
            format=self.Replay_File.split(".")[-1]
            # get file time
            if format=='asc':
                framefile = read_csv(self.Replay_File,skiprows=4,encoding="gbk",
                                    engine='python',sep=' ',delimiter=None, index_col=False,header=None,skipinitialspace=True)
                file_time=framefile.values[-3][0]
                t=int(float(file_time))
            else :          #format=='blf'
                log_data = BLFReader(self.Replay_File)
                file_start=log_data.start_timestamp
                file_end=log_data.stop_timestamp
                t=int(float(file_end)-float(file_start)) 

            self.Pause.config(state=tk.DISABLED)
            self.Continue.config(state=tk.DISABLED)
            self.list_box2.insert("end","------------------------------------------------------------------") 
            self.list_box2.insert("end",self.Replay_File+"将播放"+str(t)+"s")
            self.list_box2.insert("end",self.Replay_File+"加载中...")      
            self.list_box2.see(tk.END)                   
            # set file
            self.app_Caone.set_ReplayBlock_File(self.Replay_File)
            self.INCA.set_record_filename(self.Replay_File)     
            # start 
            self.app_Caone.start_Measurement()           
            self.INCA.start_record()
            if t<30:
                self._showProgress(t)
            else:
                self._showProgress(int(0.94*t))
            self.list_box2.insert("end",self.Replay_File+"回放并记录中...")
            self.list_box2.see(tk.END) 
            time.sleep(t) #wait data replay finish
            self.INCA.stop_record()
            self.app_Caone.stop_Measurement()  
            
            self.ProcessNum+=1
            self.list_box.delete(0)
            self.FileLists=self.FileLists[1:]
            self.text2.set("剩余需处理的文件数:  "+str(self.NumberOfFile-self.ProcessNum))
            self.list_box2.insert("end",self.Replay_File+"完成回放并保存...")
            self.list_box2.insert("end","------------------------------------------------------------------")
            self.list_box2.see(tk.END)
                
        pythoncom.CoUninitialize()
        
    def exit(self):
        answer=tk.messagebox.askokcancel('请选择','确认退出回灌程序吗？')
        if answer:   
            sys.exit()
    
    
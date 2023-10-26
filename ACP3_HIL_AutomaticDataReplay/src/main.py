import tkinter as tk
from tkinter import filedialog,messagebox
from tk_ProcessPage import ProcessPage
from ExternalCall_CANoe import *
from ExternalCall_INCA import *
import sys
import os
import time
import multiprocessing
import threading
import pythoncom
import ctypes

class LoadPage:
    def __init__(self,master) -> None:  
        current_path = os.getcwd()
        if hasattr(sys, 'frozen'):
            current_path = os.path.dirname(sys.executable)
        elif __file__:
            current_path = os.path.dirname(os.path.abspath(__file__))
        self.current_work_dir = '/'.join(current_path.split("\\")[:-1])
        
        #Variables
        self.Thread_ID_List=[]
        self.varStartFile=tk.StringVar()
        self.Start_File=self.current_work_dir+"/Normal Start_convert.blf"
        self.varStartFile.set(self.Start_File)
        self.Folder_path=''
        self.Replay_File=''
        self.text=tk.StringVar()
        self.textButton=tk.StringVar()
        self.ReplayButton=tk.StringVar()
        self.showPath=tk.StringVar()
        self.text.set("需要回灌的文件 :")
        self.textButton.set("打开文件")
        self.ReplayButton.set("回放数据")
        self.showPath.set("")
        self.pattern=tk.IntVar()
        self.pattern.set(1)
        self.thread_Flag=True
        
        #Configure
        self.root=master
        self.root.title("台架自动化回灌录制")
        self.root.geometry("900x270")
        self.bg_color='snow'
        self.fg_color="red"       
        self.root.configure(background=self.bg_color)
        
        # Create Module on window
        self.page1=tk.Frame(self.root,bg=self.bg_color)
        self.page1.pack()
        
        self.row1=tk.Frame(self.page1)
        self.row1.pack(padx=10,pady=5)
        self.row1.configure(background=self.bg_color)     
        tk.Label(self.row1, text="台架Canoe数据回灌", font="Calibri 30 bold", bg=self.bg_color, fg="red").pack(padx=0,fill='y')
       
        self.row2=tk.Frame(self.page1)
        self.row2.pack(padx=10,pady=5)
        self.row2.configure(background=self.bg_color)
        NormalStart_Label=tk.Label(self.row2,width=17,text="NormalStart文件 :", font="Calibri 12 bold", bg=self.bg_color, fg=self.fg_color)
        NormalStart_Label.pack(side = tk.LEFT,padx=5,pady=5)
        NormalStart_Path=tk.Label(self.row2,textvariable=self.varStartFile,bg='white',width=88,relief='groove',font="Calibri 10 bold")
        NormalStart_Path.pack(side = tk.LEFT,padx=5,pady=5)
        NormalStart_SelectButton=tk.Button(self.row2,text='打开文件',width=9, command=self.load_StartFile)
        NormalStart_SelectButton.pack(side = tk.LEFT,pady=5)
        
        self.row3=tk.Frame(self.page1)
        self.row3.pack(padx=10,pady=5)
        self.row3.configure(background=self.bg_color)
        tk.Label(self.row3,width=17,textvariable=self.text, font="Calibri 12 bold", bg=self.bg_color, fg=self.fg_color).pack(side = tk.LEFT,padx=5,pady=5)        
        ReplayFile=tk.Label(self.row3,textvariable=self.showPath,bg='white',width=88,relief='groove',font="Calibri 10 bold")
        ReplayFile.pack(side = tk.LEFT,padx=5,pady=5)
        NormalStart_SelectButton=tk.Button(self.row3,textvariable=self.textButton,width=9, command=self.load)
        NormalStart_SelectButton.pack(side = tk.LEFT,pady=5)
        
        self.row4=tk.Frame(self.page1)
        self.row4.pack(padx=10,pady=5)
        self.row4.configure(background=self.bg_color)
        tk.Radiobutton(self.row4, text="回灌单个文件", variable=self.pattern, value=1,command=self.changePattern,bg=self.bg_color,font="Calibri 10").pack(side='left',padx=40)
        tk.Radiobutton(self.row4, text="回灌文件夹文件", variable=self.pattern, value=2,command=self.changePattern,bg=self.bg_color,font="Calibri 10").pack(side='left')
    
        self.row5=tk.Frame(self.page1)
        self.row5.pack(padx=10,pady=15,fill=tk.BOTH) 
        self.row5.configure(background=self.bg_color)        
        tk.Button(self.row5, text='退出', command=self.exit,width=8).pack(side = tk.RIGHT,padx=4)
        tk.Button(self.row5, textvariable=self.ReplayButton, command=self.check,width=13).pack(side = tk.RIGHT,padx=10)
        self.NormalStartButton=tk.Button(self.row5, text='StartNormal', command=self._startNormal,width=13)
        self.NormalStartButton.pack(side = tk.RIGHT,padx=10)
        self.CanoeButton=tk.Button(self.row5, text='加载Canoe配置', command=self.loadCanoe,width=13)
        self.CanoeButton.pack(side = tk.RIGHT,padx=10)
    
    # Different pattern to choose replay File or Files
    def changePattern(self):
        if self.pattern.get()==1:
            self.text.set("需要回灌的文件 :")
            self.textButton.set("打开文件")
            self.ReplayButton.set("回放数据")
            self.showPath.set(self.Replay_File)
        else:
            self.text.set("批量回灌的文件夹 :")
            self.textButton.set("打开文件夹")
            self.ReplayButton.set("回放文件夹数据")
            self.showPath.set(self.Folder_path)
        
    def load_StartFile(self):
        self.Start_File = filedialog.askopenfilename()
        self.varStartFile.set(self.Start_File)
    
    def load(self):
        if self.pattern.get()==1:
            self.Replay_File = filedialog.askopenfilename()
            self.showPath.set(self.Replay_File)
        else:
            self.Folder_path = filedialog.askdirectory()
            self.showPath.set(self.Folder_path)
    
    def _startNormal(self):
        v1=threading.Thread(target=self.threadingTask)
        v1.setDaemon(True)
        v1.start()
        self.Thread_ID_List.append(v1.ident)
    
    @property   
    def startNormal(self):
        try:
            format=self.Start_File.split(".")[-1]
            if os.path.exists(self.Start_File) and (format=="blf" or format=="asc"):
                pythoncom.CoInitialize()
                self.app_Caone = CANoe()
                self.app_Caone.stop_Measurement()  
            else:
                messagebox.showerror("错误","请检查NormalStart文件格式及路径")
        except:
            messagebox.showerror("未知错误","请先打开正确的Canoe配置")
        else:
            self.NormalStartButton.config(state=tk.DISABLED)
            while True:
                t=10   
                self.app_Caone.set_ReplayBlock_File(self.Start_File)
                self.app_Caone.start_Measurement()
                time.sleep(t)
                self.app_Caone.stop_Measurement()  
                time.sleep(5)
       
    def threadingTask(self):
        p=multiprocessing.Process(target=self.startNormal)
    
    # raise exception to kill thread
    def raise_exception(self):   
        thread_id = self.Thread_ID_List[0]
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
			ctypes.py_object(SystemExit)) 
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            print('Exception raise failure')  
    
    def loadCanoe(self):
        try:
            pythoncom.CoInitialize()
            self.app_Caone = CANoe()
            self.app_Caone.stop_Measurement()
            path=self.current_work_dir+"/ACP3_HIL_AutomaticDataReplay.cfg"
            if os.path.exists(path):
                self.app_Caone.open_cfg(path)
                pythoncom.CoUninitialize()
            else:
                messagebox.showerror("错误","未找到Canoe配置路径")
        except BaseException:
            messagebox.showerror("未知错误","请手动打开Canoe配置")
           
    # Check before replay        
    def check(self):
        if self.pattern.get()==1:  # check File Format
            Flag_Start=0
            Flag_File=0
            format_StartFile=self.Start_File.split(".")[-1]
            format_ReplayFile=self.Replay_File.split(".")[-1]
            if os.path.exists(self.Start_File) and (format_StartFile=="blf" or format_StartFile=="asc"):
                Flag_Start=1
            if os.path.exists(self.Replay_File) and (format_ReplayFile=="blf" or format_ReplayFile=="asc"):
                Flag_File=1
            if not Flag_Start:   
                messagebox.showwarning(title='警告',message='请检查NormalStart文件格式及路径')
            elif not Flag_File:
                messagebox.showwarning(title='警告',message='请检查回灌数据格式，需asc或blf格式')
            else:
                try:
                    pythoncom.CoInitialize()
                    self.inca = Inca()
                    self.inca.get_openExp()
                    self.inca.stop_measurement()
                except BaseException:
                    messagebox.showwarning(title='警告',message='请先正确连接INCA')
                else:
                    if len(self.Thread_ID_List)!=0:
                        self.raise_exception()    
                    self.page1.destroy()
                    ProcessPage(self.root,self.Start_File,self.Replay_File,self.Folder_path,self.pattern.get())    
        
        else: # check StartFile Format and Filefolder
            Flag_StartFile=0
            Flag_Folder=0        
            format=self.Start_File.split(".")[-1]
            if os.path.exists(self.Start_File) and (format=="blf" or format=="asc"):
                Flag_StartFile=1           
            if os.path.exists(self.Folder_path):
                Flag_Folder=1                
            if not Flag_StartFile:   
                messagebox.showwarning(title='警告',message='请检查NormalStart文件格式及路径')
            elif not Flag_Folder:
                messagebox.showwarning(title='警告',message='请检查回灌数据文件夹路径')
            else:
                try:
                    pythoncom.CoInitialize()
                    self.inca = Inca()
                    self.inca.get_openExp()
                    self.inca.stop_measurement()
                except BaseException:
                    messagebox.showwarning(title='警告',message='请先正确连接INCA')
                else:
                    if len(self.Thread_ID_List)!=0:
                        self.raise_exception()  
                    self.page1.destroy()            
                    ProcessPage(self.root,self.Start_File,self.Replay_File,self.Folder_path,self.pattern.get())
          
    def exit(self):
        answer=tk.messagebox.askokcancel('请选择','确认退出回灌程序吗？')
        if answer:            
            sys.exit()
        else:
            pass     
 
if __name__=="__main__":
    multiprocessing.freeze_support()
    root = tk.Tk()
    LoadPage(master=root)   
    root.mainloop()

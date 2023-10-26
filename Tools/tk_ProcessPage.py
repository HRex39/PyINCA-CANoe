import tkinter as tk
from ExternalCall_CANoe import *
from ExternalCall_INCA import *
import tkinter as tk
from pandas import read_csv
from can import BLFReader
import os,sys
import time
import threading
import pythoncom
#from multiprocessing import Process,Queue,freeze_support

class ProcessPage:
    def __init__(self,master:tk.Tk,Start_File,Replay_File,Folderpath,pattern) -> None:
        self.root=master
        self.root.title("台架自动化回灌录制")
        self.root.geometry("900x620")
        self.Start_File=Start_File
        self.Replay_File=Replay_File
        self.Folderpath=Folderpath
        self.pattern=pattern  
        self.FileLists=[]
        self.ProcessNum=0
        self.message_list=[]
        self.bg_color='snow'
        self.fg_color="red"
        self.root.protocol("WM_DELETE_WINDOW", self.SafeExit)
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
              
        self.root.configure(background=self.bg_color)
        self.root=tk.Frame(self.root,bg=self.bg_color)
        self.root.pack()
        
        self.row5=tk.Frame(self.root,bd =1 ,relief = tk.SUNKEN,bg=self.bg_color)
        self.row5.pack(side = tk.BOTTOM,fill="x")
        self.row5.configure(background=self.bg_color)
        tk.Label(self.row5, text='保存位置 >>> '+self.result_path, anchor =tk.W, bg=self.bg_color, font="Calibri 11 bold").pack(side = tk.LEFT) 
        tk.Label(self.row5, text='|版权所属:ADAS标定开发股', anchor =tk.W, bg=self.bg_color, font="Calibri 10 bold").pack(side = tk.RIGHT)        
        
        self.row1=tk.Frame(self.root)
        self.row1.pack()
        self.row1.configure(background=self.bg_color) 
        tk.Label(self.row1, text="要处理的文件数:  "+str(self.NumberOfFile), font="Calibri 15 bold", bg=self.bg_color, fg="red").pack(padx=0,fill='y')
        
        self.row2=tk.Frame(self.root)
        self.row2.pack(pady=7)
        self.row2.configure(background=self.bg_color) 
        tk.Label(self.row2, text="剩余要处理的文件数:  "+str(self.NumberOfFile-self.ProcessNum), font="Calibri 15 bold", bg=self.bg_color, fg="red").pack(padx=0,fill='y')

        self.row21=tk.Frame(self.root,bd =1 ,relief = tk.SUNKEN)
        self.row21.pack(fill="x")
        self.row21.configure(background=self.bg_color) 
        tk.Label(self.row21,text='程序运行状态', width=72,borderwidth=2,relief="ridge",bg=self.bg_color, font="Calibri 11 bold").pack(side=tk.LEFT)
        tk.Label(self.row21,text='剩余文件列表', width=30,borderwidth=2,relief="ridge",bg=self.bg_color, font="Calibri 11 bold").pack(side=tk.LEFT)
        
        self.row3=tk.Frame(self.root)
        self.row3.pack(expand=tk.YES, fill=tk.BOTH)
        self.row3.configure(background=self.bg_color)
        scrollbar = tk.Scrollbar(self.row3, bg=self.bg_color)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.list_box = tk.Listbox(self.row3, width=27,height=24,selectmode="multiple", font="Arial 11", bg=self.bg_color)
        self.list_box.pack(side="right",expand=tk.YES, fill="both")
        self.list_box.config(yscrollcommand=scrollbar.set)
        scrollbarx =tk.Scrollbar(self.list_box, orient=tk.HORIZONTAL)
        scrollbarx.pack(side=tk.BOTTOM, fill=tk.BOTH)
        scrollbar.config(command=self.list_box.yview)
        scrollbarx.config(command=self.list_box.xview)
        
        scrollbar2 = tk.Scrollbar(self.row3, bg=self.bg_color)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.BOTH)       
        self.list_box2 = tk.Listbox(self.row3, width=70,height=24,selectmode="multiple", font="Arial 11", bg=self.bg_color)
        self.list_box2.pack(expand=tk.YES, fill="both")
        self.list_box2.config(yscrollcommand=scrollbar2.set)
        scrollbarx2 =tk.Scrollbar(self.row3, orient=tk.HORIZONTAL)
        scrollbarx2.pack(side=tk.BOTTOM, fill=tk.BOTH)
        scrollbar2.config(command=self.list_box2.yview)
        scrollbarx2.config(command=self.list_box2.xview)
        
        self.row4=tk.Frame(self.root)
        self.row4.pack(expand=tk.YES, fill=tk.BOTH,pady=7)
        self.row4.configure(background=self.bg_color)
        tk.Button(self.row4, text='退出', command=self.exit,width=8).pack(side = tk.RIGHT,padx=10)
        tk.Button(self.row4, text='暂停', command=None,width=8).pack(side = tk.RIGHT,padx=10)
        tk.Button(self.row4, text='继续', command=None,width=8).pack(side = tk.RIGHT,padx=10)
        
        #append FileList to list_box
        for i in self.FileLists:
            self.list_box.insert("end",i)   
        
        self._Test()    
        #self._Start()

    
    def _Test(self):
        p=threading.Thread(target=self.Test) 
        p.setDaemon(True)   # 守护--就算主界面关闭，线程也会留守后台运行（不对!）
        p.start()
    
    def Test(self):
        for i in range(30):
            time.sleep(1)
            self.list_box2.insert("end",i)        
            
     
    def _Start(self):
        p=threading.Thread(target=self.Start) 
        p.setDaemon(False)  
        p.start()

    def Start(self):
        pythoncom.CoInitialize()
        self.list_box2.insert("end","开始回灌")
        #Canoe init
        self.app_Caone = CANoe()
        # #self.app_Caone.open_cfg(r"E:\CANOE_Script\ACP3_HIL_Feedback\ACP3_HIL_Feedback.cfg") #导入某个CANoe config

        #INCA init
        self.INCA=Inca()
        self.INCA.get_openExp()
        self.INCA.set_record_path(self.result_path)
        self.INCA.start_measurement()
                  
            
        #Start_File_load
        log_data = BLFReader(self.Start_File)
        file_start = log_data.start_timestamp
        file_end = log_data.stop_timestamp
        t=int(float(file_end)-float(file_start)) 
        t=10   #Bug
        self.list_box2.insert("end","NormalStart File将播放"+str(t)+"s")
        self.list_box2.insert("end","NormalStart File加载中，请稍等...")
        self.list_box2.see(tk.END) 
        self.app_Caone.set_ReplayBlock_File(self.Start_File)
        self.INCA.start_measurement()
        self.app_Caone.start_Measurement()
        self.list_box2.insert("end","NormalStart File播放中...")
        self.list_box2.see(tk.END) 
        time.sleep(t)
        self.app_Caone.stop_Measurement()  
        time.sleep(5)
        self.list_box2.insert("end","NormalStart完成...")
        self.list_box2.insert("end"," ")
        self.list_box2.see(tk.END) 
             
        if self.pattern==2:  
            # Batch File Load
            for File in self.FileLists:
                Record_Flag=1
                format=File.split(".")[-1]
                # get file time
                if format=='asc':
                    framefile = read_csv(self.Folderpath+"/"+File,skiprows=4,encoding="gbk",
                                        engine='python',sep=' ',delimiter=None, index_col=False,header=None,skipinitialspace=True)
                    file_time=framefile.values[-3][0]
                    t=int(float(file_time))
                elif format=='blf':
                    log_data = BLFReader(self.Folderpath+"/"+File)
                    file_start=log_data.start_timestamp
                    file_end=log_data.stop_timestamp
                    t=int(float(file_end)-float(file_start)) 
                else:
                    Record_Flag=0
                    
                if Record_Flag:    
                    self.list_box2.insert("end","------------------------------------------------------------------") 
                    self.list_box2.insert("end",File+"将播放"+str(t)+"s")
                    self.list_box2.insert("end",File+"加载中...")      
                    self.list_box2.see(tk.END)                   
                    # set file
                    self.app_Caone.set_ReplayBlock_File(self.Folderpath+"/"+File)
                    self.INCA.set_record_filename(File)     
                    # start 
                    self.app_Caone.start_Measurement()           
                    self.INCA.start_record()
                    self.list_box2.insert("end",File+"回放并记录中...")
                    self.list_box2.see(tk.END) 
                    time.sleep(t) #wait data replay finish
                    self.INCA.stop_record()
                    self.app_Caone.stop_Measurement()  
                    self.ProcessNum+=1
                    self.list_box2.insert("end",File+"完成回放并保存...")
                    self.list_box2.insert("end","------------------------------------------------------------------")
                    self.list_box2.see(tk.END)           
                                
                else:
                    self.list_box2.insert("end",File+"格式不正确，跳过此文件...")    
                    self.list_box2.see(tk.END) 
            
            self.list_box2.insert("end","------------------------------------------------------------------")
            self.list_box2.insert("end","所有数据已回灌完成！！")
            self.list_box2.see(tk.END)
                    
        else: #pattern==1
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
            self.list_box2.insert("end",self.Replay_File+"回放并记录中...")
            self.list_box2.see(tk.END) 
            time.sleep(t) #wait data replay finish
            self.INCA.stop_record()
            self.app_Caone.stop_Measurement()  
            self.ProcessNum+=1
            self.list_box2.insert("end",self.Replay_File+"完成回放并保存...")
            self.list_box2.insert("end","------------------------------------------------------------------")
            self.list_box2.see(tk.END)
                
        pythoncom.CoUninitialize()
        
    def exit(self):
        answer=tk.messagebox.askokcancel('请选择','确认退出回灌程序吗？')
        if answer:   
            self.INCA.stop_measurement()
            self.INCA.stop_record()
            self.app_Caone.stop_Measurement()
            sys.exit()
            
    def SafeExit(self):
        #点击右上角退出将调用该窗口
        self.root.destroy()
        #可加入Canoe&INCA退出操作
        sys.exit(0)
    
if __name__=="__main__":
    root = tk.Tk()
    pro=ProcessPage(master=root,Start_File=r"C:\Users\llliu\Desktop\HIL\Normal Start_convert.blf",
                    Replay_File=r"C:/Users/llliu\Desktop/HIL/test_Data/{ES25IV001_2023-08-09_15-55-24}_BUS002.asc",
                    Folderpath=r"C:\Users\llliu\Desktop\HIL\test_Data",pattern=2)
    root.mainloop()
    
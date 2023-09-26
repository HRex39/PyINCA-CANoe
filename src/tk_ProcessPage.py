import tkinter as tk
from ExternalCall_CANoe import *
from ExternalCall_INCA import *
import tkinter as tk
from pandas import read_csv
from can import BLFReader
import os

class ProcessPage:
    def __init__(self,master:tk.Tk,Start_File,Folderpath) -> None:
        self.root=master
        self.root.title("台架自动化回灌录制")
        self.root.geometry("600x600")
        self.Start_File=Start_File
        self.Folderpath=Folderpath
        self.FileLists=os.listdir(self.Folderpath)
        self.NumberOfFile=len(self.FileLists)
        self.ProcessNum=0
        self.message_list=[]
        #tk.Button(self.root, text='退出', command=None).grid(row=35, column=2, padx=5, pady=5)
    
    def Start(self):
        self.message_list.append("StartProcess")
        self.showInfo()
        self.result_path=self.Folderpath+"/Result"
        if not os.path.isdir(self.result_path):
            os.mkdir(self.result_path)
    #     #Canoe init
    #     app_Caone = CANoe()
    #     # #app_Caone.open_cfg(r"E:\CANOE_Script\ACP3_HIL_Feedback\ACP3_HIL_Feedback.cfg") #导入某个CANoe config

    #     # #INCA init
    #     INCA=Inca()
    #     INCA.get_openExp()
    #     INCA.set_record_path(self.result_path)
    #     INCA.start_measurement()
        
    #     # self.message_list.append("1")
    #     # self.message_list.append("2")
    #     # self.message_list.append("3")
    #     # self.message_list.append("4")
    #     # self.message_list.append("5")
    #     # self.message_list.append("6")
    #     # self.message_list.append("77"+"ad")
    #     # self.message_list.append("8")
    #     # self.message_list.append("9")
    #     # self.message_list.append("10")
    #     # self.message_list.append("11")
    #     # self.message_list.append("12")
    #     # self.message_list.append("13")
    #     # self.message_list.append("14")
    #     # self.message_list.append("15")
    #     # self.message_list.append("16")
    #     # self.message_list.append("17")
    #     # self.message_list.append("18")
    #     # self.message_list.append("19")
        
        
    #     # #Start_File_load
    #     log_data = BLFReader(self.Start_File)
    #     file_start = log_data.start_timestamp
    #     file_end = log_data.stop_timestamp
    #     t=int(float(file_end)-float(file_start)) 
    #     self.message_list.append("NormalStart File will play about "+str(t)+"s")
    #     self.message_list.append("NormalStart File load, please wait...")
    #     app_Caone.set_ReplayBlock_File(self.Start_File)
    #     INCA.start_measurement()
    #     app_Caone.start_Measurement()
    #     time.sleep(t)
    #     app_Caone.stop_Measurement()  
    #     self.message_list.append("NormalStart done...")
    #     self.message_list.append(" ")
               
    #     # Batch File Load
    #     for File in self.FileLists:
    #         Record_Flag=1
    #         format=File.split(".")[-1]
    #         # get file time
    #         if format=='asc':
    #             framefile = read_csv(self.Folderpath+"/"+File,skiprows=4,encoding="gbk",
    #                                 engine='python',sep=' ',delimiter=None, index_col=False,header=None,skipinitialspace=True)
    #             file_time=framefile.values[-3][0]
    #             t=int(float(file_time))
    #         elif format=='blf':
    #             log_data = BLFReader(self.Folderpath+"/"+File)
    #             file_start=log_data.start_timestamp
    #             file_end=log_data.stop_timestamp
    #             t=int(float(file_end)-float(file_start)) 
    #         else:
    #             Record_Flag=0
                
    #         if Record_Flag:                
    #             self.message_list.append(File+" will record about "+str(t)+"s")       
    #             self.message_list.append(File+" is load...")                
    #             # set file
    #             app_Caone.set_ReplayBlock_File(self.Folderpath+"/"+File)
    #             INCA.set_record_filename(File)     
    #             # start 
    #             app_Caone.start_Measurement()
    #             #time.sleep(5) # No need to wait Canoe start, it will stay in this line until Canoe start measure
    #             INCA.start_record()
    #             self.message_list.append(File+" is replay and recording...")
    #             time.sleep(t) #wait data replay finish
    #             INCA.stop_record()
    #             app_Caone.stop_Measurement()  
    #             self.ProcessNum+=1
    #             self.message_list.append(File+" is done and save...")     
    #             self.message_list.append(" ")
                             
    #         else:
    #             self.message_list.append(File+" is not correct format, we will skip this file...")      
    
    def showInfo(self):
        tk.Label(self.root, text='要处理的文件数量: '+str(self.NumberOfFile),font=("黑体",12),
                 width=70).grid(row=0, column=2, padx=5, pady=5)
        tk.Label(self.root, text='剩余需要处理的文件数量: '+str(self.NumberOfFile-self.ProcessNum),
                 font=("黑体",12),width=70).grid(row=1, column=2, padx=5, pady=5)
        tk.Label(self.root,text='  ').grid(row=2, column=2, padx=5, pady=1)
        tk.Label(self.root,text='处理进度：',font=("黑体",10)).grid(row=3, column=2, padx=5, pady=1)
        
        #Process Info
        number=18
        if len(self.message_list)<number:
            for i in range(len(self.message_list)):
                tk.Label(self.root, text=self.message_list[i],
                font=("黑体",10),width=70).grid(row=(4+i), column=2, padx=5, pady=1)
        else:
            n=0
            for i in range(number,-1,-1):
                tk.Label(self.root, text=self.message_list[len(self.message_list)-1-i],
                font=("黑体",10),width=70).grid(row=(4+n), column=2, padx=5, pady=1)
                n+=1
            
                
    
    
if __name__=="__main__":
    root = tk.Tk()
    pro=ProcessPage(master=root,Start_File=r"C:\Users\llliu\Desktop\HIL\Normal Start_convert.blf",
                Folderpath=r"C:\Users\llliu\Desktop\HIL\test_Data")
    pro.showInfo()
    pro.Start()
    
    #root.mainloop()
    
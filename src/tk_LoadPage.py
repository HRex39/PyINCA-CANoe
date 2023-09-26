import tkinter as tk
from tkinter import filedialog,messagebox
from tk_ProcessPage import ProcessPage
import sys
import os
import time
import multiprocessing

class LoadPage:
    def __init__(self,master) -> None:
        self.root=master
        self.root.title("台架自动化回灌录制")
        self.root.geometry("800x400")
        self.Start_File=''
        self.Folderpath=''
        
        self.varStartFile=tk.StringVar()
        self.varFolder=tk.StringVar()
        
        self.page1=tk.Frame(self.root)
        self.page1.pack()
        tk.Label(self.page1,text='   ').grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.page1, text='NormalStart文件').grid(row=1, column=1, padx=5, pady=5)
        tk.Label(self.page1, textvariable=self.varStartFile,bg='white',width=60,relief='groove').grid(row=1, column=2, padx=5, pady=5)
        tk.Button(self.page1, text='打开文件', command=self.load_File).grid(row=1, column=3, padx=5, pady=5)

        tk.Label(self.page1, text='回灌数据所在文件夹').grid(row=2, column=1, padx=5, pady=5)
        tk.Label(self.page1, textvariable=self.varFolder,bg='white',width=60,relief='groove').grid(row=2, column=2, padx=5, pady=5)
        tk.Button(self.page1, text='打开文件夹', command=self.load_Folder).grid(row=2, column=3, padx=5, pady=5)
        
        tk.Label(self.page1,text='').grid(row=3, column=0, padx=5, pady=5)
        tk.Button(self.page1, text='开始回放和录制', command=self.check).grid(row=4, column=2, padx=5, pady=5)
        tk.Button(self.page1, text='退出', command=self.exit).grid(row=4, column=3, padx=5, pady=5)
        
    def load_File(self):
        self.Start_File = filedialog.askopenfilename()
        self.varStartFile.set(self.Start_File)
        
    def load_Folder(self):
        self.Folderpath = filedialog.askdirectory()
        self.varFolder.set(self.Folderpath)
        '''
    def StartProcess(self):
        tk.Button(self.page1, text='开始', command=self.check).grid(row=3, column=3, padx=5, pady=5)'''

    # check File
    def check(self):
        Flag_StartFile=0
        Flag_Folder=0        
        format=self.Start_File.split(".")[-1]
        
        if os.path.exists(self.Start_File) and (format=="blf" or format=="asc"):
            Flag_StartFile=1
        
        if os.path.exists(self.Folderpath):
            Flag_Folder=1
               
        if not Flag_StartFile:   
            messagebox.showwarning(title='警告',message='请检查NormalStart文件格式')
        elif not Flag_Folder:
            messagebox.showwarning(title='警告',message='请检查回灌数据文件夹路径')
        else:
            self.page1.destroy()
            processpage=ProcessPage(self.root,self.Start_File,self.Folderpath)
            processpage.showInfo()
            time.sleep(1)
            processpage.Start()
            
    
    def exit(self):
        answer=tk.messagebox.askokcancel('请选择','确认退出回灌程序吗？')
        if answer:            
            # stop INCA and Canoe
            # -------------------
            sys.exit()
        else:
            pass          
            
 
if __name__=="__main__":
    root = tk.Tk()
    LoadPage(master=root)
    root.mainloop()
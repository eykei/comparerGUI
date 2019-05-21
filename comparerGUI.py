'''
Description: Walks through two directories, and compares the files in two directories and lists files exclusive to eachother.
Usage: Use the GUI, click [+] button to select directory 1 and 2. Click Analyze.
Status: Working
ToDo: Handle paths better (getPath1 and getPath2 functions)
'''

from tkinter import *
from tkinter import filedialog
import os

largeFont=("Verdana",14)
smallFont=("Verdana",8)

def walk(path):
    fileList=[]
    count=0
    for folder, subfolder, files in os.walk(path):
        for file in files:
            filepath = os.path.join(os.path.abspath(folder), file)
            count+=1
            fileList.append(os.path.basename(filepath))
    return fileList, count


class App:
    def __init__(self, master):
        frame=Frame(master)
        frame.pack()

        Label(frame, text='Comparer v0.1',font=largeFont).grid(row=0, columnspan=7, pady=10)

        Label(frame, text='Directory 1', font=smallFont).grid(row=1, column=1, columnspan=2)
        Label(frame, text='Directory 2',font=smallFont).grid(row=1, column=4, columnspan=2)

        self.path1Var = StringVar()
        Entry(frame, textvariable=self.path1Var, width=20).grid(row=2, column=1, pady=20,sticky=W+E+N+S)

        self.path2Var = StringVar()
        Entry(frame, textvariable=self.path2Var, width=20).grid(row=2, column=4, pady=20,sticky=W+E+N+S)

        directory1Button=Button(frame,text='[+]', command=self.getPath1)
        directory1Button.grid(row=2,column=2)

        directory2Button=Button(frame,text='[+]', command=self.getPath2)
        directory2Button.grid(row=2,column=5)

        scrollbary1=Scrollbar(frame)
        scrollbary1.grid(row=3,column=2,sticky=N+S)

        scrollbary2 = Scrollbar(frame)
        scrollbary2.grid(row=3, column=5, sticky=N+S)
        
        scrollbarx1=Scrollbar(frame, orient=HORIZONTAL)
        scrollbarx1.grid(row=4,column=1,sticky=W+E)

        scrollbarx2 = Scrollbar(frame, orient=HORIZONTAL)
        scrollbarx2.grid(row=4, column=4, sticky=W+E)

        self.textBox1 = Text(frame, relief=SUNKEN, wrap=NONE, width=80, height=30,  font=smallFont, yscrollcommand=scrollbary1.set, xscrollcommand=scrollbarx1.set)
        self.textBox1.grid(row=3, column=1, sticky=W + E + N + S)

        self.textBox2 = Text(frame, relief=SUNKEN, wrap=NONE, width=80, height=30, font=smallFont, yscrollcommand=scrollbary2.set, xscrollcommand=scrollbarx2.set)
        self.textBox2.grid(row=3, column=4, sticky=W + E + N + S)

        scrollbarx1.config(command=self.textBox1.xview)
        scrollbarx2.config(command=self.textBox2.xview)

        Label(frame, text='Files in Directory 1 not in Directory 2', font=smallFont).grid(row=5,column=1, sticky=W)
        self.count12Var=DoubleVar()
        Label(frame, textvariable=self.count12Var, font=smallFont).grid(row=5, column=1)

        Label(frame, text='Files in Directory 2 not in Directory 1', font=smallFont).grid(row=5, column=4, sticky=W)
        self.count21Var=DoubleVar()
        Label(frame, textvariable=self.count21Var, font=smallFont).grid(row=5, column=4)

        Label(frame, text='Number of files in directory 1: ', font=smallFont).grid(row=6,column=1, sticky=W)
        self.count1Var=DoubleVar()
        Label(frame,textvariable=self.count1Var, font=smallFont).grid(row=6,column=1)

        Label(frame, text='Number of files in directory 2: ', font=smallFont).grid(row=6, column=4, sticky=W)
        self.count2Var = DoubleVar()
        Label(frame, textvariable=self.count2Var, font=smallFont).grid(row=6, column=4)

        analyzeButton=Button(frame, text="Analyze", command=self.analyze)
        analyzeButton.grid(row=3, column=3, pady=20, padx=20, sticky=N)

    def analyze(self):
        self.textBox1.config(state=NORMAL)  # make tables writable
        self.textBox2.config(state=NORMAL)

        self.textBox1.delete(1.0, END)  # clear the tables
        self.textBox2.delete(1.0, END)

        path1 = self.path1Var.get()  # get the directory from the entry field
        path2 = self.path2Var.get()

        list1, count1 = walk(path1)
        list2, count2 = walk(path2)

        count12 = 0
        count21 = 0

        for x in list1:
            if x not in list2:
                count12 += 1
                self.textBox1.insert(END, x+'\n')

        for y in list2:
            if y not in list1:
                count21 += 1
                self.textBox2.insert(END, y+'\n')

        self.textBox1.config(state=DISABLED)
        self.textBox2.config(state=DISABLED)

        self.count12Var.set(count12)
        self.count21Var.set(count21)

        self.count1Var.set(count1)
        self.count2Var.set(count2)

    def getPath1(self):
        path=filedialog.askdirectory()
        path=path.replace('/','\\\\')
        path += '\\\\'
        self.path1Var.set(path)

    def getPath2(self):
        path=filedialog.askdirectory()
        path=path.replace('/','\\\\')
        path += '\\\\'
        self.path2Var.set(path)


root=Tk()
root.wm_title('Comparer')
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
root.geometry(f"{w}x{h}+0+0")
app=App(root)
root.mainloop()

print('Done')
import tkinter as tk
from tkinter import ttk
from utils import log_q, hunters
from assistant import HunterAssistant

# win = tk.Tk()
# win.title("51jingying")    # 添加标题
# win.geometry('500x380')
# win.resizable(0, 0)        # 禁止调整窗口大小



# ttk.Label(win, text="Chooes a number").grid(column=1, row=0)    # 添加一个标签，并将其列设置为1，行设置为0
# ttk.Label(win, text="Enter a name:").grid(column=0, row=0)      # 设置其在界面中出现的位置  column代表列   row 代表行

# # button被点击之后会被执行
# def clickMe():   # 当acction被点击时,该函数则生效
#   action.configure(text='Hello ' + name.get())     # 设置button显示的内容
# #   action.configure(state='disabled')      # 将按钮设置为灰色状态，不可使用状态

# # 按钮
# action = ttk.Button(win, text="Click Me!", command=clickMe)     # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
# action.grid(column=2, row=1)    # 设置其在界面中出现的位置  column代表列   row 代表行

# # 文本框
# name = tk.StringVar()     # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
# nameEntered = ttk.Entry(win, width=12, textvariable=name)   # 创建一个文本框，定义长度为12个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
# nameEntered.grid(column=0, row=1)       # 设置其在界面中出现的位置  column代表列   row 代表行
# nameEntered.focus()     # 当程序运行时,光标默认会出现在该文本框中

# # 创建一个下拉列表
# number = tk.StringVar()
# numberChosen = ttk.Combobox(win, width=12, textvariable=number)
# numberChosen['values'] = (1, 2, 4, 42, 100)     # 设置下拉列表的值
# numberChosen.grid(column=1, row=1)      # 设置其在界面中出现的位置  column代表列   row 代表行
# numberChosen.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

# win.mainloop()      # 当调用mainloop()时,窗口才会显示出来


# import tkinter
# from tkinter import ttk  # 导入内部包
 
# li = ['王记','12','男']
# lis = li * 100
# root = tkinter.Tk()
# root.title('测试')
# tree = ttk.Treeview(root,columns=['1','2','3'],show='headings')
# tree.column('1',width=100,anchor='center')
# tree.column('2',width=100,anchor='center')
# tree.column('3',width=100,anchor='center')
# tree.heading('1',text='姓名')
# tree.heading('2',text='学号')
# tree.heading('3',text='性别')
# for i in lis:
#     tree.insert('','end',values=li)
# tree.grid()
 
 
# def treeviewClick(event):#单击
#     print ('单击')
#     for item in tree.selection():
#         item_text = tree.item(item,"values")
#         print(item_text[0])#输出所选行的第一列的值
 
# tree.bind('<ButtonRelease-1>', treeviewClick)#绑定单击离开事件===========
# root.mainloop()

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry('500x380')
root.title('51jingying')
root.resizable(0, 0)

sb = ttk.Scrollbar(root)
sb.pack()

lb = ttk.Listbox(root, yscrollcommand=sb.set)

scrollbar = Scrollbar(myWindow)
scrollbar.pack( side = RIGHT, fill = Y )
 
mylist = Listbox(myWindow, yscrollcommand = scrollbar.set)
for line in range(100):
    mylist.insert(END, "This is line number " + str(line))
 
mylist.pack( side = LEFT, fill = BOTH )
scrollbar.config( command = mylist.yview )
#进入消息循环
myWindow.mainloop()

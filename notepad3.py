# 导入类库
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Scrollbar, Checkbutton, Label, Button
import os
import sys

class NotePad(Tk):
    # 菜单栏下的图片名
    icons = ["new_file", "open_file", "save", "cut", "copy", "paste", "undo", "redo", "find_text"]
    icon_res = []
    
    
    # 初始化操作
    def __init__(self):
        super().__init__()
        self.file_name = None
        self.set_window()
        self.create_menu_bar()
        self.create_tool_bar()
        self.create_body()
           
    # 设置窗口界面
    def set_window(self):
        self.title("NotePad")
        max_width, max_height = self.maxsize()
        align_center = "800x600+%d+%d" % ((max_width-800)/2, (max_height-600)/2)
        self.geometry(align_center)
        self.iconbitmap("img/editor.ico")
    
    # 创建菜单项目
    def create_menu_bar(self):
        menu_bar = Menu(self)
        
        # 添加菜单项目
        
        # 文件栏
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='文件', menu=file_menu)
        
        # 文件拦下
        file_menu.add_command(label='新建', accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label='打开', accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label='保存', accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label='另存为', accelerator="Shift+Ctrl+S", command=self.save_as)
        file_menu.add_separator()  # 分隔线
        file_menu.add_command(label='退出', accelerator="Alt+F4", command=self.exit_notepad)
  
        # 编辑栏
        editor_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='编辑', menu=editor_menu)

        # 编辑栏下
        editor_menu.add_command(label='撤销', accelerator="Ctrl+Z", command='')
        editor_menu.add_command(label='恢复', accelerator="Ctrl+Y", command='')
        editor_menu.add_separator()
        editor_menu.add_command(label='剪切', accelerator="Ctrl+X", command='')
        editor_menu.add_command(label='复制', accelerator="Ctrl+C", command='')
        editor_menu.add_command(label='粘贴', accelerator="Ctrl+V", command='')
        editor_menu.add_separator()
        editor_menu.add_command(label='查找', accelerator="Ctrl+F", command='')
        editor_menu.add_separator()
        editor_menu.add_command(label='全选', accelerator="Ctrl+A", command='')
        
         
        # 视图栏
        view_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='视图', menu=view_menu)
        
        # 视图栏下
        
        # 显示行号  
        self.is_show_line_num = IntVar()
        self.is_show_line_num.set(1)
        view_menu.add_checkbutton(label="显示行号", onvalue=0, offvalue=1, variable=self.is_show_line_num, command='')
        
        # 高亮当前行
        self.is_heighlight_line = IntVar()
        view_menu.add_checkbutton(label="高亮当前行", variable=self.is_heighlight_line, command='')
        
        # 分隔
        view_menu.add_separator() 
        
        # 主题
        themes_menu = Menu(menu_bar, tearoff=0)
        # 后续实现
        themes_menu.add_command(label="主题1", command="")
        themes_menu.add_command(label="主题2", command="")
        view_menu.add_cascade(label="主题", menu=themes_menu)
        
        
        # 关于栏
        about_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='关于', menu=about_menu)
        
        # 关于栏下
        about_menu.add_command(label="关于", command="")
        about_menu.add_command(label="帮助", command="")
        
        self['menu'] = menu_bar

    # 菜单栏下图片工具功能区
    def create_tool_bar(self):
        tool_bar = Frame(self, height=25, background="#FFFFFF")
        # 填充X轴
        tool_bar.pack(fill="x")
        for icon in self.icons:
            tool_icon = PhotoImage(file="img/%s.gif" % (icon, ))
            tool_btn = Button(tool_bar, image=tool_icon, command="")
            tool_btn.pack(side="left")
            # 要将tool_icon添加到icon_res
            self.icon_res.append(tool_icon)
            

    # 界面操作的主体
    def create_body(self):
        # 左边行号，中间是文本编辑区，右边是滚动条
        self.line_number_bar = Text(self, width=4, padx=3, takefocus=0, border=0, background="#F0E68C", state="disable")
        self.line_number_bar.pack(side="left", fill="y")
        
        # 文本编辑区
        # wrap 如何换行， word表示按照单词自动换行
        # undo=True 表示开启撤销功能
        self.context_text = Text(self, wrap="word", undo=True)
        # 热键绑定
        self.context_text.bind("<Control-o>", self.open_file)
        self.context_text.bind("<Control-O>", self.open_file)
        self.context_text.bind("<Control-s>", self.save_file)
        self.context_text.bind("<Control-S>", self.save_file)
        self.context_text.bind("<Control-n>", self.new_file)
        self.context_text.bind("<Control-N>", self.new_file)    
        self.context_text.pack(fill="both", expand="yes")
        
        # 设置文本输入区
        self.context_text.tag_config("active_line", background="#EEEEE0")
        
        # 滚动条
        scroll_bar = Scrollbar(self.context_text)
        scroll_bar['command'] = self.context_text.yview
        self.context_text["yscrollcommand"] = scroll_bar.set
        scroll_bar.pack(side="right", fill="y")

        
    # 打开文件
    def open_file(self, event=None):
        # 打开文件并进行类型设置
        input_file = filedialog.askopenfilename(filetypes=[("所有文件", "*"), ("文本文档", "*.txt")])
        if input_file:
            self.title("{} - NotePad".format(os.path.basename(input_file)))
            self.file_name = input_file
            self.context_text.delete(1.0, END)
            with open(input_file, 'r') as _file:
                self.context_text.insert(1.0, _file.read())
                

    # 文件的保存
    def write_to_file(self, file_name):
        try:
            content = self.context_text.get(1.0, END)
            with open(file_name, 'w') as _file:
                _file.write(content)
            self.title("{} ~ NotePad".format(os.path.basename(file_name)))
        except IOError:
            messagebox.showerror("错误", "文件保存失败！ ")

    # 保存文件
    def save_file(self, event=None):
        if not self.file_name:
            self.save_as()
        else:
            self.write_to_file(self.file_name)
    
    # 新建
    def new_file(self, event=None):
        self.title("新建 - Notepad")
        self.context_text.delete(1.0, END)
        self.file_name = None

    # 另存为
    def save_as(self):
        input_file = filedialog.askopenfilename(filetypes=[("所有文件", "*"), ("文本文档", "*.txt")])
        
        if input_file:
            self.file_name = input_file
            self.write_to_file(self.file_name)
        
    # 退出
    def exit_notepad(self):
        if messagebox.askokcancel("退出", "确定退出吗？ "):
            self.destroy()
    
if __name__ == '__main__':
    app = NotePad()
    app.mainloop()

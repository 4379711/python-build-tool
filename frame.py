import sys
import tkinter
from datetime import datetime
from functools import partial
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk, filedialog

from do_work import Work
from reg_password import *


class Application:
    text_pane = None

    def __init__(self):
        Application.check_expire_date(expire_date)
        Application.check_psd()
        self.work = Work()
        self.work.say_func = Application.write_text
        root = tkinter.Tk()
        root.title("OCR识别")
        root.geometry("600x400")
        root.resizable(False, False)
        # self.root.iconbitmap("favicon.ico")
        self.frame_left = tkinter.Frame(root, height=1500, width=300)
        self.frame_left.pack(side=tkinter.LEFT)
        self.frame_right = tkinter.Frame(root, height=1500, width=800)
        self.frame_right.pack(side=tkinter.RIGHT)
        self.create_widgets()
        root.mainloop()

    @staticmethod
    def check_expire_date(number):
        now = datetime.now().strftime('%Y%m%d')
        if int(now) > number:
            messagebox.showerror("到期提示", "您的使用期限已到，请联系管理员")
            sys.exit()

    @staticmethod
    def check_psd():
        psd = get_value(register_key)
        # 未设置过,提示设置密码
        if psd is None:
            tmp = simpledialog.askstring("", "请输入密码", show='*')
            if tmp is None:
                sys.exit()
            if tmp == register_password:
                set_value(register_key, tmp)
            else:
                tt = messagebox.askretrycancel("密码错误", "安装密码错误")
                if not tt:
                    sys.exit()
                return Application.check_psd()

    @staticmethod
    def get_filenames(component, *args):
        Work.file_path = filedialog.askopenfilenames(filetypes=[('pdf', '*.pdf'), ("all", "*.*")])
        if Work.file_path:
            for i in Work.file_path:
                Application.write_text(i)

    @staticmethod
    def get_excel_filename(component, *args):
        Work.excel_path = filedialog.askopenfilename(filetypes=[('excel', ('*.xls', '*.xlsx')), ("all", "*.*")])
        if Work.excel_path:
            Application.write_text(Work.excel_path)

    @staticmethod
    def combobox(component, *args):
        Work.combox = component.get()
        Application.write_text(Work.combox)

    def build_button_choice_file(self):
        _bt = tkinter.Button(self.frame_left, bd=0, relief='ridge', text='选择识别pdf', width=10, height=1)
        # 单击鼠标左键
        _bt.bind("<Button-1>", partial(self.get_filenames, _bt))
        _bt.pack(padx=10, pady=10)

    def build_button_choice_excel_file(self):
        _bt = tkinter.Button(self.frame_left, bd=0, relief='ridge', text='选择对比xls', width=10, height=1)
        # 单击鼠标左键
        _bt.bind("<Button-1>", partial(self.get_excel_filename, _bt))
        _bt.pack(padx=10, pady=10)

    def build_combobox(self):
        _combox = ttk.Combobox(self.frame_left,
                               state="readonly",
                               values=["通用表格识别", "买方确认函", "付款确认书", "保理商通知书"],
                               height=1,
                               width=10)
        _combox.current(0)
        Work.combox = _combox.get()
        self.write_text(_combox.get())
        _combox.bind("<<ComboboxSelected>>", partial(self.combobox, _combox))
        _combox.pack(padx=10, pady=10)

    @staticmethod
    def write_text(text):
        # now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S: ")
        if Application.text_pane is not None:
            now = datetime.strftime(datetime.now(), "%H:%M:%S")
            Application.text_pane.insert(END, f"""{now}: {text}\n""")
            Application.text_pane.see(END)

    def build_text(self):
        Application.text_pane = tkinter.Text(self.frame_right, height=100, width=100)
        Application.text_pane.pack(padx=10, pady=10)

    def choice(self, _bt, *args):
        self.work.main(_bt)

    def build_start(self):
        _bt = tkinter.Button(self.frame_left, bd=0, relief='ridge', text='开始识别', width=10, height=1)
        # 单击鼠标左键
        _bt.bind("<Button-1>", partial(self.choice, _bt))
        _bt.pack(padx=10, pady=10)

    def create_widgets(self):
        self.build_text()
        self.build_button_choice_excel_file()
        self.build_button_choice_file()
        self.build_combobox()
        self.build_start()


if __name__ == '__main__':
    Application()

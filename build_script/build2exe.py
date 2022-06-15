# -*- coding: utf-8 -*-
# @Author  : YaLong
# @File    : build2exe.py
import os
import shutil

from PyInstaller.__main__ import run


def cp_file(root_path: str, cp_file_type_list: list, dist_dir_path: str):
    def deal_files(_files):
        for name in _files:
            path = os.path.join(root, name)
            if os.path.isfile(path):
                _type = path.split(".")[-1]
                if _type in cp_file_type_list:
                    print("copy file: ", path, "--->", dist_dir_path + name)
                    shutil.copy(path, dist_dir_path + name)

    for root, dirs, files in os.walk(root_path, topdown=False):
        deal_files(files)
        deal_files(dirs)


def remove_file(root_path: str, rm_file_type_list: list, keep_list: list = None):
    def deal_files(_files):
        for name in _files:
            if keep_list is not None and name in keep_list:
                continue
            path = os.path.join(root, name)
            if os.path.isfile(path):
                _type = path.split(".")[-1]
                if _type in rm_file_type_list:
                    print("remove file:", path)
                    os.remove(path)

    for root, dirs, files in os.walk(root_path, topdown=False):
        deal_files(files)
        deal_files(dirs)


if __name__ == '__main__':
    # 删除上次编译生成的文件
    shutil.rmtree("./build", ignore_errors=True)
    shutil.rmtree("./dist", ignore_errors=True)

    # py文件编译为pyd
    # 可以用pyinstxtractor.py反编译exe查看是否用的pyd.如果是用的py,打包后会变成pyc
    # --inplace参数 把编译后的文件放到当前路径下
    # os.system("python build2pyd.py build_ext --inplace")
    os.system("python build2pyd.py build_ext")

    # 复制main.py文件到生成的pyd当前路径下
    # 注意main.py中必须导入所有依赖库,不然用pyd打包会缺少依赖库
    shutil.copy("../main.py", "./build/lib.win-amd64-3.10/main.py")

    # 打包为exe
    # opts = ['./build/lib.win-amd64-3.10/main.py', '-F', "--uac-admin", '-i=ico.ico']
    opts = ['./build/lib.win-amd64-3.10/main.py', '-D', '-w', "--uac-admin"]
    run(opts)

    # 删除生成的临时文件
    remove_file(root_path="../", rm_file_type_list=["c", "spec"])

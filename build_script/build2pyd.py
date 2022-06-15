import os
import sys

from Cython.Build import cythonize
from setuptools import setup, Extension


def find_file(root_path: str, cp_file_type_list: list):
    def deal_files(_files):
        tmp = []
        for name in _files:
            # 排除这个文件
            if name == "__init__.py":
                continue
            path = os.path.join(root, name)
            if os.path.isfile(path):
                _type = path.split(".")[-1]
                if _type in cp_file_type_list:
                    tmp.append(path)
        return tmp

    result = []
    for root, dirs, files in os.walk(root_path, topdown=False):
        tmp_ = deal_files(files) + deal_files(dirs)
        result += tmp_
    return result


# 要编译的模块
extensions = [
    # 参数: 模块名 ,模块下的文件
    Extension("frame", ["../frame.py"]),
    Extension("api", ["../api.py"]),
    Extension("do_work", ["../do_work.py"]),
    Extension("reg_password", ["../reg_password.py"]),
    Extension("split_pdf", ["../split_pdf.py"]),
    Extension("config", ["../config.py"]),
    Extension("excel_utils", ["../excel_utils.py"]),
]

setup(
    ext_modules=cythonize(
        module_list=extensions,
        # 指定编译版本为Python-3
        compiler_directives={'language_level': sys.version_info[0]})
)

# 安装c++ build tools
# pip install setuptools
# pip install cython

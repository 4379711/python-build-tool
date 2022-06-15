import os

import fitz

# img_path 图像要保存的文件夹
img_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.img')


def clear_img():
    if not os.path.exists(img_dir_path):
        return
    for i in os.listdir(img_dir_path):
        os.remove(os.path.join(img_dir_path, i))


def pdf_image(pdf_path):
    """
    pip install pymupdf
    将PDF转化为图片
    pdfPath pdf文件的路径
    """
    if not os.path.exists(img_dir_path):
        os.mkdir(img_dir_path)
    # 存储图片地址
    path_list = []
    # 如果不是pdf文件，认为是图片，直接添加到列表中
    if not pdf_path.endswith('.pdf'):
        path_list.append(pdf_path)
        return path_list
    # 打开PDF文件
    pdf = fitz.open(pdf_path)
    pdf_name = os.path.basename(pdf_path)
    # 逐页读取PDF
    for pg in range(0, pdf.pageCount):
        page = pdf[pg]
        # 设置缩放和旋转系数
        trans = fitz.Matrix(1, 1).prerotate(0)
        pm = page.get_pixmap(matrix=trans, alpha=False)
        # 开始写图像
        _path = f"{img_dir_path}//{pdf_name}_{str(pg)}.jpg"
        pm.save(_path)
        path_list.append(_path)
    pdf.close()
    return path_list


if __name__ == '__main__':
    dir_path = r"C:\Users\admin\Documents\WeChat Files\wxid_oom6ei15ggmv22\FileStorage\File\2022-05\底稿示例\底稿示例\付款确认书\需转换文件"

    # pdf_image(dir_path + r"\WKGXH220112001.pdf")
    # clear_img()

import re
from functools import partial
from threading import Thread, Lock

from api import Api
from excel_utils import *
from split_pdf import *


class Work:
    # ["买方确认函", "付款确认书", "银行回单"]
    combox = None
    # ("C://A.pdf", "C://B.pdf")
    file_path = None
    excel_path = None
    has_click = False
    lock = Lock()
    api = Api()
    say_func = print
    money_re = re.compile("\d+\.?\d*")
    int_re = re.compile("\d")
    error_number = -999.99

    def get_money(self, text):
        money_list = self.money_re.findall(str(text))
        try:
            return float(''.join(money_list))
        except Exception:
            return Work.error_number

    def get_int(self, text):
        int_list = self.int_re.findall(str(text))
        if len(int_list) != 1:
            return Work.error_number
        try:
            return int(int_list[0])
        except Exception:
            return Work.error_number

    def common_table(self, pic_path_list, add_filename_column, file_name):
        """
       把几个图片的表格,合并成一个表格
        :param file_name: 要保存的excel文件名
       :param pic_path_list: 图片列表
       :param add_filename_column: 是否添加文件名列
       """
        we = WriteExcel()
        last_table_row = 0
        for pic_path in pic_path_list:
            resp = ''
            try:
                resp = self.api.table(pic_path)
                # 文件名
                pic_file_name = os.path.basename(pic_path).split(".")[0]
                block_list = resp["result"]["blocks"]
                for block in block_list:
                    # 表格最大行
                    table_max_row = 0
                    # 只提取表格
                    if block["is_table"]:
                        end_row_list = set()
                        for cell in block["cells"]:
                            tmp_end_row = cell["end_row"]
                            we.add(cell["start_row"] + last_table_row, cell["end_row"] + last_table_row,
                                   cell["start_column"], cell["end_column"], cell["text"].replace("\n", ""))
                            # 把这个表格的最大行记录下来
                            table_max_row = max(table_max_row, tmp_end_row)
                            end_row_list.add(cell["end_row"])
                        # 额外添加一列文件名
                        if add_filename_column:
                            for row in end_row_list:
                                we.add(row + last_table_row, row + last_table_row, 5, 5, pic_file_name)
                        # 识别完一个表格后,更新行号到最后一行,其他表格的行追加
                        last_table_row = last_table_row + table_max_row + 1
            except Exception as e:
                self.say_func(resp)
                self.say_func(pic_path, e)

        # 创建保存识别结果的文件夹
        p_path = os.path.dirname(Work.file_path[0])
        __file_ppath = os.path.join(p_path, "识别结果")
        if not os.path.exists(__file_ppath):
            os.makedirs(__file_ppath)
        # 先删除文件,再保存
        result_xlsx_path = os.path.join(__file_ppath, file_name)
        if os.path.exists(result_xlsx_path):
            os.remove(result_xlsx_path)
        we.save(result_xlsx_path)
        return result_xlsx_path

    @staticmethod
    def get_pdf_path_by_name_prefix(name_prefix):
        for i in Work.file_path:
            if name_prefix in i:
                return i

    def compare(self):
        # 检查文件
        if not Work.excel_path:
            self.say_func("未选择文件对比的excel文件")
            return
        ce = ChangeExcel(Work.excel_path)
        all_pdf_data_dict = {}
        # 识别的发票编号放在第10列
        _column_0 = 11
        # 识别的发票金额放在第11列
        _column_1 = 12
        # 识别的应收账款转让金额放在第12列
        _column_2 = 13
        # 对比结果放在第13列
        result_column = 14

        # excel转list
        old_excel_data_list = excel_to_list_ffill(Work.excel_path)
        print(old_excel_data_list)
        for excel_row_num in range(len(old_excel_data_list)):
            excel_row = old_excel_data_list[excel_row_num]
            pdf_name_prefix = excel_row[0]
            # 防止重复识别
            if pdf_name_prefix not in all_pdf_data_dict.keys():
                pdf_path = self.get_pdf_path_by_name_prefix(pdf_name_prefix)
                if not pdf_path:
                    self.say_func("未找到文件:%s" % pdf_name_prefix)
                    ce.change(excel_row_num + 1, result_column, '未找到pdf文件')
                    ce.save()
                    continue
                # 先清空图片文件夹,留备份文件
                clear_img()
                self.say_func(f"开始识别{pdf_path}")
                pic_path_list = pdf_image(pdf_path)
                self.say_func(f"共切分出{len(pic_path_list)}张图片")
                self.say_func("开始识别表格")
                xlsx_path = self.common_table(pic_path_list, False, f"{pdf_name_prefix}.xlsx")
                self.say_func("备份excel存放在:")
                self.say_func(xlsx_path)
                # 要对比的表格
                tmp_list = excel_to_list_ffill(xlsx_path)
                # 结果存起来后对比
                all_pdf_data_dict[pdf_name_prefix] = tmp_list
            # 识别的表格结果
            tmp_list = all_pdf_data_dict[pdf_name_prefix]
            left_line_result = False
            fapiao_all_result = False
            yingshou_all_result = False
            result_str = '对比失败'
            _column_0_list = []
            _column_1_list = []
            _column_2_list = []
            for table_row in tmp_list:
                if len(table_row) < 9:
                    result_str = 'pdf表格格式无法识别'
                    break
                print(1, excel_row[2] == table_row[1])
                print(2, excel_row[3] == table_row[2])
                print(3, excel_row[4] == table_row[3])
                print(4, excel_row[5] == table_row[4])
                print(5, excel_row[6] == table_row[5])
                print(6, excel_row[7], self.get_money(table_row[6]))
                print(7, excel_row[8], self.get_money(table_row[7]))

                # 把发票金额数据记录
                if self.get_int(table_row[0]) != Work.error_number:
                    _column_0_list.append(str(table_row[5]))
                    _column_1_list.append(str(self.get_money(table_row[6])))
                    _column_2_list.append(str(self.get_money(table_row[7])))

                if excel_row[2] == table_row[1] and \
                        excel_row[3] == table_row[2] and \
                        excel_row[4] == table_row[3] and \
                        excel_row[5] == table_row[4]:
                    left_line_result = True
                maybe_money = [self.get_money(p) for p in table_row if self.get_money(p) != Work.error_number]
                if '发票金额合计' in table_row[0] and float(excel_row[9]) in maybe_money:
                    fapiao_all_result = True
                if '应收账款' in table_row[0] and float(excel_row[10]) in maybe_money:
                    yingshou_all_result = True
                print(left_line_result, fapiao_all_result, yingshou_all_result)

            # 识别的发票编号	识别的发票金额	识别的应收账款转让金额 这三列汇总写入excel
            ce.change(excel_row_num + 1, _column_0, ",".join(_column_0_list))
            ce.change(excel_row_num + 1, _column_1, ",".join(_column_1_list))
            ce.change(excel_row_num + 1, _column_2, ",".join(_column_2_list))

            # 汇总这一行的对比结果
            if left_line_result and fapiao_all_result and yingshou_all_result:
                result_str = '对比成功'
            ce.change(excel_row_num + 1, result_column, result_str)
            ce.save()

    def run(self):
        if not Work.file_path:
            self.say_func("未选择文件")
            return

        if Work.combox == "买方确认函":
            """
            一次选多个pdf,每个pdf切图片,把所有图片的所有表格,汇总成一个excel
            """
            # 先清空图片文件夹
            clear_img()
            self.say_func("开始切分pdf为图片")
            pic_path_list = []
            for _file_path in Work.file_path:
                _tmp_list = pdf_image(_file_path)
                pic_path_list.extend(_tmp_list)
            self.say_func(f"共切分出{len(pic_path_list)}张图片")
            self.say_func("开始识别表格")
            xlsx_path = self.common_table(pic_path_list, True, "result.xlsx")
            self.say_func("生成excel完成存放在:")
            self.say_func(xlsx_path)
        elif Work.combox == "通用表格识别" or Work.combox == "付款确认书":
            """
            每次选多个pdf,每个pdf切多个图片,把每个pdf里面的所有表格,汇总成一个excel,每个pdf生成一个excel
            """
            for pdf_file_path in Work.file_path:
                # 获取文件名
                pdf_file_name = os.path.basename(pdf_file_path)
                # 每次清空图片文件夹
                clear_img()
                self.say_func(f"{pdf_file_name}开始切分pdf为图片")
                pic_path_list = pdf_image(pdf_file_path)
                self.say_func(f"{pdf_file_name}共切分出{len(pic_path_list)}张图片")
                self.say_func("开始识别表格")
                xlsx_path = self.common_table(pic_path_list, False, f"{pdf_file_name}.xlsx")
                self.say_func("生成excel完成存放在:")
                self.say_func(xlsx_path)
        elif Work.combox == "保理商通知书":
            self.compare()

    def warp(self, component, func):
        old = component["text"]
        component["text"] = "正在识别"
        # 设置不可点击
        component["state"] = "disabled"
        try:
            self.say_func("开始识别")
            func()
            self.say_func("识别完成")
        except Exception as e:
            self.say_func(f"识别失败{e}")
            raise e
        finally:
            component["text"] = old
            # 恢复可点击
            component["state"] = "active"
            Work.has_click = False
            self.say_func("*" * 50)
            Work.file_path = None
            Work.excel_path = None

    def main(self, component):
        with self.lock:
            if Work.has_click:
                self.say_func("正在识别中,请稍后再试")
            else:
                Work.has_click = True
                Thread(target=partial(self.warp, component, self.run)).start()

# import pandas as pd
#
# # 显示所有列
# pd.set_option('display.max_columns', None)
# # 显示所有行
# pd.set_option('display.max_rows', 30)
# # 设置显示宽度是无限
# pd.set_option('display.width', None)
# tmp_excel_data = pd.read_excel(r"C:\Users\admin\Downloads\合合AI-表格识别导出.xlsx")
# tmp_excel_data.replace('\n', '', regex=True, inplace=True)
# tmp_excel_data.fillna(method='ffill', inplace=True)
# tmp_list = tmp_excel_data.values.tolist()
# print(tmp_list)
#
# import re
#
# # 提取金额
#
# money_re = re.compile("(\d+\.?\d*)")
# money_list = money_re.findall("人民币(小写):2,252,285.83元")
# print(''.join(money_list))
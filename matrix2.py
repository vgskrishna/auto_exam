# matrix2.py

import pandas as pd
import numpy as np
import xlsxwriter


def missing(missing, st_list):
    for i in missing:
        for j in st_list:
            if j == i:
                st_list.remove(i)
    return st_list

def run(el_list, ec_list, it_list, col, row):
    temp_matrix = []
    while it_list or el_list or ec_list:
        temp_matrix.append(ec_list[:1])
        ec_list = ec_list[1:]
        temp_matrix.append(el_list[:1])
        el_list = el_list[1:]
        temp_matrix.append(it_list[:1])
        it_list = it_list[1:]
    
    matrix = []
    for i in range(row):
        a = []
        for j in range(col):
            b = temp_matrix[:1]
            b = str(b)[1:-1]
            b = str(b)[1:-1]
            a.append(b)
            temp_matrix = temp_matrix[1:]
        matrix.append(a)
    
    Result = []
    for i in range(col):
        b = []
        for j in range(row):
            b.append(0)
        Result.append(b)
    
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            Result[j][i] = matrix[i][j]
    
    return Result



# def write(result, room_no):
#     data = result
#     filename = 'static/execl/' + room_no + '.xlsx'
#     workbook = xlsxwriter.Workbook(filename)
#     worksheet = workbook.add_worksheet(room_no)

#     for row_num, row_data in enumerate(data):
#         worksheet.write_row(row_num, 0, row_data)

#     workbook.close()

# def write(result, room_no):
#     data = result
#     filename = 'static/execl/' + room_no + '.xlsx'
#     workbook = xlsxwriter.Workbook(filename)
#     worksheet = workbook.add_worksheet(room_no)

#     for row_num, row_data in enumerate(data):
#         worksheet.write_row(row_num, 0, row_data)

#     workbook.close()

def write(result, room_no):
    data = result
    df = pd.DataFrame(data)
    df.to_excel('static/execl/' + room_no + '.xlsx', header=None, index=False)



def read(room_no):
    pd.options.display.float_format = '{:,.0f}'.format
    temp = pd.read_excel('static/execl/'+room_no+'.xlsx', header=None, index_col=False).astype(str).replace(to_replace="nan", value=0)
    temp = temp.replace(to_replace=0, value="Blank")
    return temp

# Example additional function:
def calculate_average(data):
    return data.mean()

# Example additional variable:
max_students = 50

# You can add more functions or variables as per your requirements.

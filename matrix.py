

import os
import xlsxwriter
import pandas as pd
import openpyxl


def missing(missing, st_list):

    for i in missing:
        for j in st_list:
            if (j == i):
                st_list.remove(i)
    return st_list


def saveRoomNo(room_no, result):
    result_data = {
        'matrix': result,
        'room_no': room_no
    }

    return result_data


def run(el_list, ec_list, it_list, col, row, room_no):
    el = len(el_list)
    ec = len(ec_list)
    it = len(it_list)
    temp_matrix = []
    while (it_list != [] or el_list != [] or ec_list != []):
        if (it == ec == el):
            temp_matrix.append(ec_list[:1])
            ec_list = ec_list[1:]
            temp_matrix.append(el_list[:1])
            el_list = el_list[1:]
            temp_matrix.append(it_list[:1])
            it_list = it_list[1:]
        elif (el >= ec) and (el > it):
            if (ec > it):
                if (it_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(ec_list[:1])
                    ec_list = ec_list[1:]
                    temp_matrix.append(it_list[:1])
                    it_list = it_list[1:]
                elif (ec_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(ec_list[:1])
                    ec_list = ec_list[1:]
                elif (el_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(it_list[:1])
                    it_list = it_list[1:]
            elif (it > ec):
                if (ec_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(ec_list[:1])
                    ec_list = ec_list[1:]
                    temp_matrix.append(it_list[:1])
                    it_list = it_list[1:]
                elif (it_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(it_list[:1])
                    it_list = it_list[1:]
                elif (el_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(ec_list[:1])
                    ec_list = ec_list[1:]
        elif (ec >= it) and (ec > el):
            if (el > it):
                if (it_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(ec_list[:1])
                    ec_list = ec_list[1:]
                    temp_matrix.append(it_list[:1])
                    it_list = it_list[1:]
                elif (el_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(ec_list[:1])
                    ec_list = ec_list[1:]
                elif (ec_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(ec_list[:1])
                    ec_list = ec_list[1:]
            elif (it > el):
                if (el_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(ec_list[:1])
                    ec_list = ec_list[1:]
                    temp_matrix.append(it_list[:1])
                    it_list = it_list[1:]
                elif (it_list != []):
                    temp_matrix.append(it_list[:1])
                    it_list = it_list[1:]
                    temp_matrix.append(ec_list[:1])
                    ec_list = ec_list[1:]
                elif (ec_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(ec_list[:1])
                    ec_list = ec_list[1:]
        elif (it >= el) and (it > ec):
            if (ec > el):
                if (el_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(ec_list[:1])
                    ec_list = ec_list[1:]
                    temp_matrix.append(it_list[:1])
                    it_list = it_list[1:]
                elif (ec_list != []):
                    temp_matrix.append(ec_list[:1])
                    ec_list = ec_list[1:]
                    temp_matrix.append(it_list[:1])
                    it_list = it_list[1:]
                elif (it_list != []):
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(it_list[:1])
                    it_list = it_list[1:]

            elif (el > ec):
                if (ec_list != []):
                    temp_matrix.append(it_list[:1])
                    it_list = it_list[1:]
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(ec_list[:1])
                    ec_list = ec_list[1:]

                elif (el_list != []):
                    temp_matrix.append(it_list[:1])
                    it_list = it_list[1:]
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                elif (it_list != []):
                    temp_matrix.append(it_list[:1])
                    it_list = it_list[1:]
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]
                    temp_matrix.append(el_list[:1])
                    el_list = el_list[1:]

    matrix = []
    for i in range(row):  # A for loop for row entries
        a = []
        for j in range(col):  # A for loop for column entries
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
    saveRoomNo(room_no, Result)

    return Result


# def write(result,room_no):
#     data = result
#     writer = pd.ExcelWriter('static/execl/'+room_no+'.xlsx', engine='xlsxwriter')
#     df = pd.DataFrame(data)
#     df.to_excel(writer, sheet_name=room_no,header=None,index=False)
#     writer.save()

def write(result, room_no):
    data = result
    filename = 'static/execl/' + room_no + '.xlsx'
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet(room_no)

    for row_num, row_data in enumerate(data):
        worksheet.write_row(row_num, 0, row_data)

    workbook.close()


def find_allocated_room(roll_number):
    excel_files = os.listdir('static/execl')
    for excel_file in excel_files:
        if excel_file.endswith('.xlsx'):
            try:
                # Read the Excel file into a Pandas DataFrame
                df = pd.read_excel(os.path.join('static/execl', excel_file))

                # Check if the roll number is in the DataFrame
                if roll_number in df.values:
                    # Return the Excel file's name (room number)
                    return excel_file
            except pd.errors.ParserError:
                pass  # Handle parsing errors if necessary
    return None


def read(room_no):
    temp = pd.read_excel('static/execl/'+room_no+'.xlsx',
                         header=None, index_col=False).astype(str)
    return temp

# def write(result, room_no):
#     data = result
#     filename = 'static/execl/' + room_no + '.xlsx'
#     workbook = xlsxwriter.Workbook(filename)
#     worksheet = workbook.add_worksheet(room_no)

#     for row_num, row_data in enumerate(data):
#         worksheet.write_row(row_num, 0, row_data)

#     workbook.close()  # Use close() to save the workbook


def read(room_no):
    temp = pd.read_excel('static/execl/'+room_no+'.xlsx',
                         header=None, index_col=False).astype(str)
    return temp

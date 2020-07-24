import openpyxl

class Utils:
    def __init__(self):
        self.ext_txt = ".txt"
        self.ext_dat = ".dat"
        self.ext_xlsx = ".xlsx"

    def csv_to_list_ignr_header(self, path, deli_str=","):
        result_list =[]
        with open(path, "r") as f:
            header = f.readline()
            print(header)
            while True:
                tmp_line = f.readline().replace("\n", "")
                if tmp_line == '':
                    break

                result_list.append(tmp_line.split(deli_str))
        return result_list


    def make_excel_indel_frequency_by_cell_id(self, path, data_dict, names):
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        row = 1
        sheet.cell(row=row, column=1, value='')
        sheet.cell(row=row, column=2, value=names[0] + '_cnt')
        sheet.cell(row=row, column=3, value='')
        sheet.cell(row=row, column=4, value=names[1] + '_cnt')

        row += 1
        sheet.cell(row=row, column=1, value='mut')
        sheet.cell(row=row, column=2, value=data_dict['main_mut_cnt'][0])
        sheet.cell(row=row, column=3, value='mut')
        sheet.cell(row=row, column=4, value=data_dict['main_mut_cnt'][1])

        row += 1
        sheet.cell(row=row, column=1, value='')
        sheet.cell(row=row, column=2, value='')
        sheet.cell(row=row, column=3, value='non_mut')
        sheet.cell(row=row, column=4, value=data_dict['main_mut_cnt'][2])

        row += 1
        sheet.cell(row=row, column=1, value='non_mut')
        sheet.cell(row=row, column=2, value=data_dict['main_non_mut_cnt'][0])
        sheet.cell(row=row, column=3, value='mut')
        sheet.cell(row=row, column=4, value=data_dict['main_non_mut_cnt'][1])

        row += 1
        sheet.cell(row=row, column=1, value='')
        sheet.cell(row=row, column=2, value='')
        sheet.cell(row=row, column=3, value='non_mut')
        sheet.cell(row=row, column=4, value=data_dict['main_non_mut_cnt'][2])

        workbook.save(filename=path + self.ext_xlsx)

    def make_excel_err_list(self, path, data_list):
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        row = 1
        for data_arr in data_list[::-1]:
            col = 1
            for data_val in data_arr:
                sheet.cell(row=row, column=col, value=str(data_val))
                col += 1
            row += 1

        workbook.save(filename=path + self.ext_xlsx)




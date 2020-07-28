import openpyxl

import Logic
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

    def make_excel_homo_hetero(self, path, trgt_list, id_list):
        logic = Logic.Logics()

        workbook = openpyxl.Workbook()
        sheet = workbook.active

        main_mut_dict = trgt_list[0][0]
        main_non_mut_dict = trgt_list[0][1]
        sub_mut_dict = trgt_list[1][0]
        sub_non_mut_dict = trgt_list[1][1]

        row = 1
        sheet.cell(row=row, column=1, value='index')
        sheet.cell(row=row, column=2, value='barcode_1')
        sheet.cell(row=row, column=3, value='barcode_2')
        sheet.cell(row=row, column=4, value='homo_hetero')
        sheet.cell(row=row, column=5, value='main_NGS_read')
        sheet.cell(row=row, column=6, value='indel_flag')
        sheet.cell(row=row, column=7, value='#of_read')
        sheet.cell(row=row, column=8, value='sub_homo_hetero')
        sheet.cell(row=row, column=9, value='sub_NGS_read')
        sheet.cell(row=row, column=10, value='sub_indel_flag')
        sheet.cell(row=row, column=11, value='sub_#of_read')

        for cell_id in id_list:
            main_homo_hetero = logic.check_homo_hetero(cell_id, main_mut_dict, main_non_mut_dict)
            sub_homo_hetero = logic.check_homo_hetero(cell_id, sub_mut_dict, sub_non_mut_dict)
            if main_homo_hetero == "":
                if sub_homo_hetero == "":
                    continue
                else:
                    # TODO non_cat_list
                    continue

            if cell_id in main_mut_dict:
                main_row = row
                for data_arr in main_mut_dict[cell_id]:
                    main_row += 1
                    sheet.cell(row=main_row, column=4, value=main_homo_hetero)
                    sheet.cell(row=main_row, column=5, value=data_arr[0])
                    sheet.cell(row=main_row, column=6, value='O')
                    sheet.cell(row=main_row, column=7, value=data_arr[7])
                sub_row = row
                if cell_id in sub_mut_dict:
                    for data_arr in sub_mut_dict[cell_id]:
                        sub_row += 1
                        sheet.cell(row=sub_row, column=8, value=sub_homo_hetero)
                        sheet.cell(row=sub_row, column=9, value=data_arr[0])
                        sheet.cell(row=sub_row, column=10, value='O')
                        sheet.cell(row=sub_row, column=11, value=data_arr[7])
                if cell_id in sub_non_mut_dict:
                    for data_arr in sub_non_mut_dict[cell_id]:
                        sub_row += 1
                        sheet.cell(row=sub_row, column=8, value=sub_homo_hetero)
                        sheet.cell(row=sub_row, column=9, value=data_arr[0])
                        sheet.cell(row=sub_row, column=10, value='X')
                        sheet.cell(row=sub_row, column=11, value=data_arr[7])
                tmp_row = row + 1
                row = main_row
                if main_row < sub_row:
                    row = sub_row
                for idx_row in range(tmp_row, row + 1):
                    sheet.cell(row=idx_row, column=1, value=str(idx_row - 1))
                    sheet.cell(row=idx_row, column=2, value=cell_id.split("^")[0])
                    sheet.cell(row=idx_row, column=3, value=cell_id.split("^")[1])

            if cell_id in main_non_mut_dict:
                main_row = row
                for data_arr in main_non_mut_dict[cell_id]:
                    main_row += 1
                    sheet.cell(row=main_row, column=4, value=main_homo_hetero)
                    sheet.cell(row=main_row, column=5, value=data_arr[0])
                    sheet.cell(row=main_row, column=6, value='X')
                    sheet.cell(row=main_row, column=7, value=data_arr[7])
                sub_row = row
                if cell_id in sub_mut_dict:
                    for data_arr in sub_mut_dict[cell_id]:
                        sub_row += 1
                        sheet.cell(row=sub_row, column=8, value=sub_homo_hetero)
                        sheet.cell(row=sub_row, column=9, value=data_arr[0])
                        sheet.cell(row=sub_row, column=10, value='O')
                        sheet.cell(row=sub_row, column=11, value=data_arr[7])
                if cell_id in sub_non_mut_dict:
                    for data_arr in sub_non_mut_dict[cell_id]:
                        sub_row += 1
                        sheet.cell(row=sub_row, column=8, value=sub_homo_hetero)
                        sheet.cell(row=sub_row, column=9, value=data_arr[0])
                        sheet.cell(row=sub_row, column=10, value='X')
                        sheet.cell(row=sub_row, column=11, value=data_arr[7])
                tmp_row = row + 1
                row = main_row
                if main_row < sub_row:
                    row = sub_row
                for idx_row in range(tmp_row, row + 1):
                    sheet.cell(row=idx_row, column=1, value=str(idx_row - 1))
                    sheet.cell(row=idx_row, column=2, value=cell_id.split("^")[0])
                    sheet.cell(row=idx_row, column=3, value=cell_id.split("^")[1])


        workbook.save(filename=path + self.ext_xlsx)





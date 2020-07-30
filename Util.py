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
        sheet.cell(row=row, column=1, value='homo_homo')
        sheet.cell(row=row, column=2, value='homo_hetero')
        sheet.cell(row=row, column=3, value='homo_wt')
        sheet.cell(row=row, column=4, value='hetero_homo')
        sheet.cell(row=row, column=5, value='hetero_hetero')
        sheet.cell(row=row, column=6, value='hetero_wt')
        sheet.cell(row=row, column=7, value='wt_homo')
        sheet.cell(row=row, column=8, value='wt_hetero')
        sheet.cell(row=row, column=9, value='wt_wt')

        row = 4
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

        cell_non_junk_list = []
        non_cell_junk_list = []
        cnt_homo_hetero_wt = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for cell_id in id_list:
            index = 1

            # filter out cell_none or none_cell junks
            main_homo_hetero = logic.check_homo_hetero(cell_id, main_mut_dict, main_non_mut_dict)
            sub_homo_hetero = logic.check_homo_hetero(cell_id, sub_mut_dict, sub_non_mut_dict)
            if main_homo_hetero == "":
                if sub_homo_hetero == "":
                    continue
                else:  # filter out cell_none junks
                    logic.add_junk_list(cell_id, sub_mut_dict, sub_non_mut_dict, non_cell_junk_list)
                    continue
            # filter out none_cell junks
            if sub_homo_hetero == "":
                logic.add_junk_list(cell_id, main_mut_dict, main_non_mut_dict, cell_non_junk_list)
                continue

            logic.count_homo_hetero_wt(main_homo_hetero, sub_homo_hetero, cnt_homo_hetero_wt)

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
                    sheet.cell(row=idx_row, column=1, value=str(index))
                    sheet.cell(row=idx_row, column=2, value=cell_id.split("^")[0])
                    sheet.cell(row=idx_row, column=3, value=cell_id.split("^")[1])
                    index += 1

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
                    sheet.cell(row=idx_row, column=1, value=str(index))
                    sheet.cell(row=idx_row, column=2, value=cell_id.split("^")[0])
                    sheet.cell(row=idx_row, column=3, value=cell_id.split("^")[1])
                    index += 1
            # blank row by cell_id
            row += 1

        for cnt_h_h_w in range(len(cnt_homo_hetero_wt)):
            sheet.cell(row=2, column=(cnt_h_h_w + 1), value=cnt_homo_hetero_wt[cnt_h_h_w])

        workbook.save(filename=path + self.ext_xlsx)

        return [cell_non_junk_list, non_cell_junk_list]

    def make_excel_by_arr_list(self, path, data_list):
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        row = 1
        sheet.cell(row=row, column=1, value='barcode_1')
        sheet.cell(row=row, column=2, value='barcode_2')
        sheet.cell(row=row, column=3, value='indel_flag')
        sheet.cell(row=row, column=4, value='Aligned_Sequence')
        sheet.cell(row=row, column=5, value='Reference_Sequence')
        sheet.cell(row=row, column=6, value='Reference_Name')
        sheet.cell(row=row, column=7, value='Read_Status')
        sheet.cell(row=row, column=8, value='n_deleted')
        sheet.cell(row=row, column=9, value='n_inserted')
        sheet.cell(row=row, column=10, value='n_mutated')
        sheet.cell(row=row, column=11, value='#Reads')
        sheet.cell(row=row, column=12, value='%Reads')

        for data_arr in data_list:
            barcode_pair = data_arr[0].split("^")
            mut_list = data_arr[1]
            non_mut_list = data_arr[2]

            for tmp_arr in mut_list:
                row += 1
                sheet.cell(row=row, column=1, value=barcode_pair[0])
                sheet.cell(row=row, column=2, value=barcode_pair[1])
                sheet.cell(row=row, column=3, value='O')
                col = 4
                for tmp_data in tmp_arr:
                    sheet.cell(row=row, column=col, value=tmp_data)
                    col += 1

            for tmp_arr in non_mut_list:
                row += 1
                sheet.cell(row=row, column=1, value=barcode_pair[0])
                sheet.cell(row=row, column=2, value=barcode_pair[1])
                sheet.cell(row=row, column=3, value='X')
                col = 4
                for tmp_data in tmp_arr:
                    sheet.cell(row=row, column=col, value=tmp_data)
                    col += 1

        workbook.save(filename=path + self.ext_xlsx)

    def make_excel_hom_hete_filter_out_by_frequency(self, path, trgt_list, id_list, freq_arr):
        logic = Logic.Logics()

        workbook = openpyxl.Workbook()
        sheet = workbook.active

        main_mut_dict = trgt_list[0][0]
        main_non_mut_dict = trgt_list[0][1]
        sub_mut_dict = trgt_list[1][0]
        sub_non_mut_dict = trgt_list[1][1]

        threshold_main_freq = freq_arr[0]
        threshold_sub_freq = freq_arr[1]

        row = 1
        sheet.cell(row=row, column=1, value='homo_homo')
        sheet.cell(row=row, column=2, value='homo_hetero')
        sheet.cell(row=row, column=3, value='homo_wt')
        sheet.cell(row=row, column=4, value='hetero_homo')
        sheet.cell(row=row, column=5, value='hetero_hetero')
        sheet.cell(row=row, column=6, value='hetero_wt')
        sheet.cell(row=row, column=7, value='wt_homo')
        sheet.cell(row=row, column=8, value='wt_hetero')
        sheet.cell(row=row, column=9, value='wt_wt')

        row = 4
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

        cell_non_junk_list = []
        non_cell_junk_list = []
        cnt_homo_hetero_wt = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for cell_id in id_list:
            index = 1

            # filter out cell_none or none_cell junks
            main_homo_hetero = logic.check_homo_hetero(cell_id, main_mut_dict, main_non_mut_dict)
            sub_homo_hetero = logic.check_homo_hetero(cell_id, sub_mut_dict, sub_non_mut_dict)
            if main_homo_hetero == "":
                if sub_homo_hetero == "":
                    continue
                else:  # filter out cell_none junks
                    logic.add_junk_list(cell_id, sub_mut_dict, sub_non_mut_dict, non_cell_junk_list)
                    continue
            # filter out none_cell junks
            if sub_homo_hetero == "":
                logic.add_junk_list(cell_id, main_mut_dict, main_non_mut_dict, cell_non_junk_list)
                continue

            # filter out by threshold
            len_main_mut, len_main_non = logic.count_freq_by_cell(cell_id, main_mut_dict, main_non_mut_dict)
            len_sub_mut, len_sub_non = logic.count_freq_by_cell(cell_id, sub_mut_dict, sub_non_mut_dict)
            if len_main_mut + len_main_non <= threshold_main_freq:
                continue
            if len_sub_mut + len_sub_non <= threshold_sub_freq:
                continue

            logic.count_homo_hetero_wt(main_homo_hetero, sub_homo_hetero, cnt_homo_hetero_wt)

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
                    sheet.cell(row=idx_row, column=1, value=str(index))
                    sheet.cell(row=idx_row, column=2, value=cell_id.split("^")[0])
                    sheet.cell(row=idx_row, column=3, value=cell_id.split("^")[1])
                    index += 1

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
                    sheet.cell(row=idx_row, column=1, value=str(index))
                    sheet.cell(row=idx_row, column=2, value=cell_id.split("^")[0])
                    sheet.cell(row=idx_row, column=3, value=cell_id.split("^")[1])
                    index += 1
            # blank row by cell_id
            row += 1

        for cnt_h_h_w in range(len(cnt_homo_hetero_wt)):
            sheet.cell(row=2, column=(cnt_h_h_w + 1), value=cnt_homo_hetero_wt[cnt_h_h_w])

        workbook.save(filename=path + self.ext_xlsx)

        return [cell_non_junk_list, non_cell_junk_list]



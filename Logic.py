import re

class Logics:
    def __init__(self):
        self.homo = "homo"
        self.hetero = "hetero"
        self.wt = "wild_type"
        self.deli = "^"
        self.percent = 100

    """
    :param
        main_list = [mut_dict, non_mut_dict]
        sub_list = [mut_dict, non_mut_dict]
    """
    def count_len_arr_mut_non_mut_by_main_list(self, main_list, sub_list):
        main_mut_dict = main_list[0]
        main_non_mut_dict = main_list[1]
        sub_mut_dict = sub_list[0]
        sub_non_mut_dict = sub_list[1]

        # result_dict = {"main_mut_cnt": [total_mut, sub_mut, sub_non_mut], "main_non_mut_cnt": [0, 0, 0]}
        result_dict = {"main_mut_cnt": [0, 0, 0], "main_non_mut_cnt": [0, 0, 0]}
        for cell_id, val_arr in main_mut_dict.items():
            result_dict["main_mut_cnt"][0] += len(val_arr)
            if cell_id in sub_mut_dict:
                result_dict["main_mut_cnt"][1] += len(sub_mut_dict[cell_id])
            if cell_id in sub_non_mut_dict:
                result_dict["main_mut_cnt"][2] += len(sub_non_mut_dict[cell_id])

        for cell_id, val_arr in main_non_mut_dict.items():
            result_dict["main_non_mut_cnt"][0] += len(val_arr)
            if cell_id in sub_mut_dict:
                result_dict["main_non_mut_cnt"][1] += len(sub_mut_dict[cell_id])
            if cell_id in sub_non_mut_dict:
                result_dict["main_non_mut_cnt"][2] += len(sub_non_mut_dict[cell_id])

        return result_dict

    def count_cell_mut_non_mut_by_main_list(self, main_list, sub_list):
        main_mut_dict = main_list[0]
        main_non_mut_dict = main_list[1]
        sub_mut_dict = sub_list[0]
        sub_non_mut_dict = sub_list[1]

        # result_dict = {"main_mut_cnt": [total_mut, trp53_mut, trp53_non_mut], "main_non_mut_cnt": [0, 0, 0]}
        result_dict = {"main_mut_cnt": [0, 0, 0], "main_non_mut_cnt": [0, 0, 0]}
        for cell_id, val_arr in main_mut_dict.items():
            result_dict["main_mut_cnt"][0] += 1
            if cell_id in sub_mut_dict:
                result_dict["main_mut_cnt"][1] += 1
            if cell_id in sub_non_mut_dict:
                result_dict["main_mut_cnt"][2] += 1

        for cell_id, val_arr in main_non_mut_dict.items():
            result_dict["main_non_mut_cnt"][0] += 1
            if cell_id in sub_mut_dict:
                result_dict["main_non_mut_cnt"][1] += 1
            if cell_id in sub_non_mut_dict:
                result_dict["main_non_mut_cnt"][2] += 1

        return result_dict

    def count_num_by_err(self, data_list):
        err_cnt_arr = [0, 0, 0, 0, 0]

        for data_arr in data_list:
            err_str = data_arr[-1]
            if "large_indel" in err_str:
                err_cnt_arr[0] += 1
            elif "no_brcd1" in err_str:
                err_cnt_arr[1] += 1
            elif "wrong_pos_const2_strt" in err_str:
                err_cnt_arr[2] += 1
            elif "no_brcd2" in err_str:
                err_cnt_arr[3] += 1
            elif "no_const2" in err_str:
                err_cnt_arr[4] += 1
        # append col names
        data_list.append(
            ["Aligned_Sequence", "Reference_Sequence", "Reference_Name", "Read_Status", "n_deleted", "n_inserted",
             "n_mutated", "#Reads", "%Reads", "error"])
        # blank row
        data_list.append([""])
        data_list.append(err_cnt_arr)
        data_list.append(["large_indel", "no_brcd1", "wrong_pos_const2_strt", "no_brcd2", "no_const2"])

    def check_homo_hetero(self, cell_id, mut_dict, non_mut_dict):
        if cell_id in mut_dict:
            if cell_id in non_mut_dict:
                return self.hetero
            else:
                return self.homo
        else:
            if cell_id in non_mut_dict:
                return self.wt
            else:
                return ""

    def count_freq_by_cell(self, cell_id, mut_dict, non_mut_dict):
        if cell_id in mut_dict:
            if cell_id in non_mut_dict:
                return self.tot_num_of_read_by_cell(mut_dict[cell_id]), self.tot_num_of_read_by_cell(
                    non_mut_dict[cell_id])
            else:
                return self.tot_num_of_read_by_cell(mut_dict[cell_id]), 0
        else:
            if cell_id in non_mut_dict:
                return 0, self.tot_num_of_read_by_cell(non_mut_dict[cell_id])
            else:
                return 0, 0

    def count_homo_hetero_wt(self, main_type, sub_type, cnt_homo_hetero_wt):
        if main_type == self.homo:
            if sub_type == self.homo:
                cnt_homo_hetero_wt[0] += 1
            elif sub_type == self.hetero:
                cnt_homo_hetero_wt[1] += 1
            else:
                cnt_homo_hetero_wt[2] += 1
        elif main_type == self.hetero:
            if sub_type == self.homo:
                cnt_homo_hetero_wt[3] += 1
            elif sub_type == self.hetero:
                cnt_homo_hetero_wt[4] += 1
            else:
                cnt_homo_hetero_wt[5] += 1
        else:
            if sub_type == self.homo:
                cnt_homo_hetero_wt[6] += 1
            elif sub_type == self.hetero:
                cnt_homo_hetero_wt[7] += 1
            else:
                cnt_homo_hetero_wt[8] += 1

    def add_junk_list(self, cell_id, mut_dict, non_mut_dict, junk_list):
        tmp_arr = [cell_id]
        if cell_id in mut_dict:
            tmp_arr.append(mut_dict[cell_id])
        else:
            tmp_arr.append([])
        if cell_id in non_mut_dict:
            tmp_arr.append(non_mut_dict[cell_id])
        else:
            tmp_arr.append([])
        junk_list.append(tmp_arr)

    def tot_num_of_read_by_cell(self, data_list):
        cnt = 0
        for data_arr in data_list:
            cnt += int(data_arr[7])
        return cnt

    def get_num_of_reads_percent_of_read_by_cell(self, trgt_list, id_list, thres_arr):
        result_list = []

        main_mut_dict = trgt_list[0][0]
        main_non_mut_dict = trgt_list[0][1]
        sub_mut_dict = trgt_list[1][0]
        sub_non_mut_dict = trgt_list[1][1]

        threshold_main_freq = thres_arr[0]
        threshold_sub_freq = thres_arr[1]

        cell_non_junk_list = []
        non_cell_junk_list = []
        cnt_homo_hetero_wt = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        row = 0
        for cell_id in id_list:

            # filter out cell_none or none_cell junks
            main_homo_hetero = self.check_homo_hetero(cell_id, main_mut_dict, main_non_mut_dict)
            sub_homo_hetero = self.check_homo_hetero(cell_id, sub_mut_dict, sub_non_mut_dict)
            if main_homo_hetero == "":
                if sub_homo_hetero == "":
                    continue
                else:  # filter out cell_none junks
                    self.add_junk_list(cell_id, sub_mut_dict, sub_non_mut_dict, non_cell_junk_list)
                    continue
            # filter out none_cell junks
            if sub_homo_hetero == "":
                self.add_junk_list(cell_id, main_mut_dict, main_non_mut_dict, cell_non_junk_list)
                continue

            # filter out by threshold
            len_main_mut, len_main_non = self.count_freq_by_cell(cell_id, main_mut_dict, main_non_mut_dict)
            len_sub_mut, len_sub_non = self.count_freq_by_cell(cell_id, sub_mut_dict, sub_non_mut_dict)
            if len_main_mut + len_main_non <= threshold_main_freq:
                continue
            if len_sub_mut + len_sub_non <= threshold_sub_freq:
                continue

            self.count_homo_hetero_wt(main_homo_hetero, sub_homo_hetero, cnt_homo_hetero_wt)

            row += 1
            barcd1 = cell_id.split(self.deli)[0]
            barcd2 = cell_id.split(self.deli)[1]
            tmp_row = [row, barcd1, barcd2, main_homo_hetero, len_main_mut,
                       len_main_mut * self.percent / (len_main_mut + len_main_non), len_main_non,
                       len_main_non * self.percent / (len_main_mut + len_main_non), len_main_mut + len_main_non,
                       sub_homo_hetero, len_sub_mut, len_sub_mut * self.percent / (len_sub_mut + len_sub_non),
                       len_sub_non, len_sub_non * self.percent / (len_sub_mut + len_sub_non), len_sub_mut + len_sub_non]

            result_list.append(tmp_row)

        return result_list, cnt_homo_hetero_wt, [cell_non_junk_list, non_cell_junk_list]

    def count_by_range(self, data_list, trgt_idx, rng_size=10, rng_strt=0, rng_e=100):
        result_dict = {}
        for idx in range(rng_strt, rng_e, rng_size):
            result_dict.update({str(idx) + self.deli + str(idx + rng_size): 0})

        total = 0
        for data_arr in data_list:
            tmp_data = data_arr[trgt_idx]
            if tmp_data == rng_e:
                result_dict[str(rng_e - rng_size) + self.deli + str(rng_e)] += 1
                total += 1
            else:
                for range_key, val in result_dict.items():
                    try:
                        range_arr = re.findall('\d+', range_key)
                        if float(range_arr[0]) <= tmp_data < float(range_arr[1]):
                            result_dict[range_key] += 1
                            total += 1
                    except Exception as err:
                        print("err during counting data : ", err)
        result_dict.update({"total": total})
        return result_dict







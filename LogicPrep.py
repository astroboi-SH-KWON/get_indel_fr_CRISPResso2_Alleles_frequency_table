
class LogicPreps:

    def __init__(self):
        self.ext_fa = ".fa"
        self.ext_dat = ".dat"
        self.ext_gtf = ".gtf"

    def make_arr_list_to_list(self, arr_list):
        return [tmp_arr[0] for tmp_arr in arr_list]

    def make_cell_id(self, brcd_arr, deli_str):
        result_list = []
        for brcd1 in brcd_arr:
            for brcd2 in brcd_arr:
                result_list.append(brcd1 + deli_str + brcd2)

        return result_list

    def sort_list_by_ele(self, data_list, ele_idx, up_down_flag=True):
        result_list = []
        for tmp_arr in sorted(data_list, key=lambda tmp_arr: tmp_arr[ele_idx], reverse=up_down_flag):
            result_list.append(tmp_arr)
        return result_list

    def get_data_by_cell_id(self, data_list, brcd_arr, init_arr):
        mut_dict = {}
        non_mut_dict = {}
        err_list = []

        pos_brcd1_strt = init_arr[0]
        pos_brcd1_end = init_arr[1]
        gap_arr = init_arr[2]
        const1_seq = init_arr[3]
        const2_seq = init_arr[4]
        err_range = init_arr[5]
        len_brcd = pos_brcd1_end - pos_brcd1_strt
        len_from_brcd1_to_const2 = len_brcd + len(const1_seq) + len_brcd + len(const2_seq) - err_range

        for data_arr in data_list:
            Aligned_Sequence = data_arr[0]
            Ali_Sequence_wo_needle = Aligned_Sequence.replace("-", "")
            Reference_Sequence = data_arr[1]
            Reference_Name = data_arr[2]
            Read_Status = data_arr[3]
            n_deleted = int(data_arr[4])
            n_inserted = int(data_arr[5])
            n_mutated = data_arr[6]
            n_Reads = data_arr[7]
            rtio_Reads = data_arr[8]

            # detect large indel
            if Reference_Sequence.find("-"*len_from_brcd1_to_const2) != 0:
                data_arr.append("large_indel")
                err_list.append(data_arr)
                continue

            brcd1 = Ali_Sequence_wo_needle[pos_brcd1_strt: pos_brcd1_end]
            if brcd1 not in brcd_arr:
                data_arr.append("no_brcd1")
                err_list.append(data_arr)
                continue

            brcd2 = ""
            try:
                pos_const2_strt = Ali_Sequence_wo_needle.index(const2_seq)
                if (pos_brcd1_end + len(const1_seq) + len_brcd - err_range) < pos_const2_strt > (pos_brcd1_end + len(gap_arr) - 1 + len(const1_seq) + len_brcd):
                    data_arr.append("wrong_pos_const2_strt : [ " + str(pos_const2_strt) + " ]")
                    err_list.append(data_arr)
                    continue

                brcd2 += Ali_Sequence_wo_needle[pos_const2_strt - len_brcd: pos_const2_strt]
                if brcd2 not in brcd_arr:
                    data_arr.append("no_brcd2")
                    err_list.append(data_arr)
                    continue

            except Exception as err:
                data_arr.append("no_const2 : " + str(err))
                err_list.append(data_arr)
                continue

            cell_id = brcd1 + "^" + brcd2

            # check mut or not by n_deleted , n_inserted and ignore sub
            if n_deleted > 0 or n_inserted > 0:
                if cell_id in mut_dict:
                    mut_dict[cell_id].append(data_arr)
                else:
                    mut_dict.update({cell_id: [data_arr]})
            else:
                if cell_id in non_mut_dict:
                    non_mut_dict[cell_id].append(data_arr)
                else:
                    non_mut_dict.update({cell_id: [data_arr]})

        return [mut_dict, non_mut_dict], err_list

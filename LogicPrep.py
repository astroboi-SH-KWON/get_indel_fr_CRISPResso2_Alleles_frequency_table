from Bio import SeqIO
import re

import Logic
import Util

class LogicPreps:

    def __init__(self):
        self.ext_fa = ".fa"
        self.ext_dat = ".dat"
        self.ext_gtf = ".gtf"

    def make_arr_list_to_list(self, arr_list):
        return [tmp_arr[0] for tmp_arr in arr_list]

    def get_data_by_cell_id(self, data_list, brcd_arr, init_arr):
        mut_dict = {}
        non_mut_dict = {}
        err_list = []

        pos_brcd1_strt = init_arr[0]
        pos_brcd1_end = init_arr[1]
        gap_arr = init_arr[2]
        const1_seq = init_arr[3]
        const2_seq = init_arr[4]
        len_brcd = pos_brcd1_end - pos_brcd1_strt

        for data_arr in data_list:
            Aligned_Sequence = data_arr[0]
            Ali_Sequence_wo_ = Aligned_Sequence.replace("-", "")
            Reference_Sequence = data_arr[1]
            Reference_Name = data_arr[2]
            Read_Status = data_arr[3]
            n_deleted = data_arr[4]
            n_inserted = data_arr[5]
            n_mutated = data_arr[6]
            n_Reads = data_arr[7]
            rtio_Reads = data_arr[8]

            brcd1 = Ali_Sequence_wo_[pos_brcd1_strt: pos_brcd1_end]
            if brcd1 not in brcd_arr:
                data_arr.append("no_brcd1")
                err_list.append(data_arr)
                continue

            brcd2 = ""
            try:
                pos_const2_strt = Ali_Sequence_wo_.index(const2_seq)
                if (pos_brcd1_end + len(const1_seq) + len_brcd) < pos_const2_strt > (pos_brcd1_end + len(gap_arr) - 1 + len(const1_seq) + len_brcd):
                    data_arr.append("wrong_pos_const2_strt : " + str(pos_const2_strt))
                    err_list.append(data_arr)
                    continue

                brcd2 += Ali_Sequence_wo_[pos_const2_strt - len_brcd: pos_const2_strt]
                if brcd2 not in brcd_arr:
                    data_arr.append("no_brcd2")
                    err_list.append(data_arr)
                    continue

            except Exception as err:
                data_arr.append("no_const2 : " + str(err))
                err_list.append(data_arr)
                continue

            cell_id = brcd1 + "^" + brcd2
            print(Ali_Sequence_wo_)
            print(len(brcd1))
            print(brcd2)







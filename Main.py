import time

import Util
import Logic
import LogicPrep
############### start to set env ################
WORK_DIR = "D:/000_WORK/JangHyeWon_KimMinYung/20200703/WORK_DIR/"
# WORK_DIR = os.getcwd() + "/"
PROJECT_NAME = WORK_DIR.split("/")[-2]
INPUT = "input/"
F_TABLE_FILE = "/Alleles_frequency_table.txt"
BRCD_FILE = "barcode_list.txt"
POS_BRCD1_STRT = 0
POS_BRCD1_END = 9
GAP_ARR = [0, 1, 2, 3]
CONST1 = "AGTACGTACGAGTC"  # 14 bp
CONST2 = "GTACTCGCAGTAGTC"  # 15 bp

ERR_RANGE = 2
CONST_INIT = [POS_BRCD1_STRT, POS_BRCD1_END, GAP_ARR, CONST1, CONST2, ERR_RANGE]

MAIN_DIR = "TGCCATGGAGGAGTCACAGT"
SUB_DIR = "AGAGGACAGTCAGCTCCAAG"
MAIN_SUB_NAME = ["trp53", "fancg"]
############### end setting env #################
def anlyze_indel_by_MAIN_to_SUB():
    util = Util.Utils()
    logic_prep = LogicPrep.LogicPreps()
    logic = Logic.Logics()

    brcd_list = util.csv_to_list_ignr_header(WORK_DIR + INPUT + BRCD_FILE)
    brcd_arr = logic_prep.make_arr_list_to_list(brcd_list)

    trgt_list = []
    trgt_err_list = []
    for path in [MAIN_DIR, SUB_DIR]:
        csv_list = util.csv_to_list_ignr_header(WORK_DIR + INPUT + path + F_TABLE_FILE, "\t")
        result_list, err_list = logic_prep.get_data_by_cell_id(csv_list, brcd_arr, CONST_INIT)
        trgt_list.append(result_list)
        trgt_err_list.append(err_list)

    # result_dict = logic.count_len_arr_mut_non_mut_by_main_list(trgt_list[0], trgt_list[1], brcd_arr)
    result_dict = logic.count_cell_mut_non_mut_by_main_list(trgt_list[0], trgt_list[1], brcd_arr)
    util.make_excel_indel_frequency_by_cell_id(
        WORK_DIR + "output/result_indel_" + MAIN_SUB_NAME[0] + "_" + MAIN_SUB_NAME[1], result_dict, MAIN_SUB_NAME)

    for idx in range(len(trgt_err_list)):
        sorted_err_list = logic_prep.sort_list_by_ele(trgt_err_list[idx], -1)
        logic.count_num_by_err(sorted_err_list)
        util.make_excel_err_list(WORK_DIR + "output/" + MAIN_SUB_NAME[idx] + "_error_list", sorted_err_list)

def anlyze_indel_by_MAIN_to_SUB_from_list():
    util = Util.Utils()
    logic_prep = LogicPrep.LogicPreps()
    logic = Logic.Logics()

    brcd_list = util.csv_to_list_ignr_header(WORK_DIR + INPUT + BRCD_FILE)
    brcd_arr = logic_prep.make_arr_list_to_list(brcd_list)

    """
    [['Trp53', 'GE_327_Pool_S0_L001_R1_001.fastq', 'GE_327_Pool_S0_L001_R2_001.fastq', 'CCTACACTTTCAGAATTTAATTTCCCTACTGGATGTCCCACCTTCTTTTTATTCTACCCTTTCCTATAAGCCATAGGGGTTTGTTTGTTTGTATGTTTTTTAATTGACAAGTTATGCATCCATACAGTACACAATCTCTTCTCTCTACAGATGACTGCCATGGAGGAGTCACAGTCGGATATCAGCCTCGAGCTCCCTCTGAGCCAGGAGACATTTTCAGGCTTATGGAAACTGTGAGTGGATCTT', 'TGCCATGGAGGAGTCACAGT']
    , ['FANCG', 'GE_327_Pool_S0_L001_R1_001.fastq', 'GE_327_Pool_S0_L001_R2_001.fastq', 'TCTTCAGTGAAAGCCTGGACTAGGCTAGCCCTCAGGATTATACAATTACAGAGGACAGTCAGCTCCAAGGGGAGAGCGGGGACAGCAGCAGGGAGTCCTGGAGCGACAGGATGCTGGTCTCACAGGCTGTCCCATGAAACACAGCCCAAATGGTTTCCAACCCAGAGACCAACCCCACTCCAACCAAGGCTTCAAGAAGGAATTCAGTTTTTGCTCAGACAACTTTGGAAAGAGCAGGAAGTTCT', 'AGAGGACAGTCAGCTCCAAG']
    , ..., [gene, fastq_r1, fastq_r2, amplicon_seq, guide_seq]]
    """
    var_list = util.csv_to_list_ignr_header(WORK_DIR + INPUT + "var_list.txt", "\t")

    for idx in range(int(len(var_list)/2)):
        main_idx = 2*idx
        sub_idx = 2*idx + 1
        main_arr = var_list[main_idx]
        sub_arr = var_list[sub_idx]

        main_sub_nm = [main_arr[0], sub_arr[0]]
        main_path = main_arr[4] + "/CRISPResso_on_" + main_arr[1].replace(".fastq", "") + "_" + main_arr[2].replace(".fastq", "")
        sub_path = sub_arr[4] + "/CRISPResso_on_" + sub_arr[1].replace(".fastq", "") + "_" + sub_arr[2].replace(".fastq", "")
        path_arr = [main_path, sub_path]

        trgt_list = []
        trgt_err_list = []
        for path in path_arr:
            csv_list = util.csv_to_list_ignr_header(WORK_DIR + INPUT + path + F_TABLE_FILE, "\t")
            result_list, err_list = logic_prep.get_data_by_cell_id(csv_list, brcd_arr, CONST_INIT)
            trgt_list.append(result_list)
            trgt_err_list.append(err_list)

        result_dict = logic.count_cell_mut_non_mut_by_main_list(trgt_list[0], trgt_list[1], brcd_arr)
        util.make_excel_indel_frequency_by_cell_id(
            WORK_DIR + "output/result_indel_" + main_sub_nm[0] + "_" + main_sub_nm[1] + "_" + str(idx), result_dict, main_sub_nm)

        for tmp_idx in range(len(trgt_err_list)):
            sorted_err_list = logic_prep.sort_list_by_ele(trgt_err_list[tmp_idx], -1)
            logic.count_num_by_err(sorted_err_list)
            util.make_excel_err_list(WORK_DIR + "output/" + main_sub_nm[tmp_idx] + "_error_list_" + str(idx), sorted_err_list)






if __name__ == '__main__':
    start_time = time.perf_counter()
    print("start [ " + PROJECT_NAME + " ]>>>>>>>>>>>>>>>>>>")
    anlyze_indel_by_MAIN_to_SUB_from_list()  # 2
    # anlyze_indel_by_MAIN_to_SUB()  # 1
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.perf_counter() - start_time))
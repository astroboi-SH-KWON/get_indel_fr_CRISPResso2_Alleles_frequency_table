import time
import os



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
Trp53 = "TGCCATGGAGGAGTCACAGT"
FANCG = "AGAGGACAGTCAGCTCCAAG"
POS_BRCD1_STRT = 0
POS_BRCD1_END = 9
GAP_ARR = [0, 1, 2, 3]
CONST1 = "AGTACGTACGAGTC"  # 14 bp
CONST2 = "GTACTCGCAGTAGTC"  # 15 bp

ERR_RANGE = 2
CONST_INIT = [POS_BRCD1_STRT, POS_BRCD1_END, GAP_ARR, CONST1, CONST2, ERR_RANGE]

############### end setting env #################
def main():
    util = Util.Utils()
    logic_prep = LogicPrep.LogicPreps()
    logic = Logic.Logics()

    brcd_list = util.csv_to_list_ignr_header(WORK_DIR + INPUT + BRCD_FILE)
    brcd_arr = logic_prep.make_arr_list_to_list(brcd_list)

    trp53_list = util.csv_to_list_ignr_header(WORK_DIR + INPUT + Trp53 + F_TABLE_FILE, "\t")
    trp53_result_list, trp53_err_list = logic_prep.get_data_by_cell_id(trp53_list, brcd_arr,
                                                                       CONST_INIT)

    fancg_list = util.csv_to_list_ignr_header(WORK_DIR + INPUT + FANCG + F_TABLE_FILE, "\t")
    fancg_result_list, fancg_err_list = logic_prep.get_data_by_cell_id(fancg_list, brcd_arr,
                                                                                        CONST_INIT)

    # result_dict = logic.count_len_arr_mut_non_mut_by_main_list(trp53_result_list, fancg_result_list, brcd_arr)
    result_dict = logic.count_cell_mut_non_mut_by_main_list(trp53_result_list, fancg_result_list, brcd_arr)
    util.make_excel_indel_frequency_by_cell_id(WORK_DIR + "output/result_indel_frequency_by_cell_id", result_dict)

    err_list = [trp53_err_list, fancg_err_list]
    for idx in range(len(err_list)):
        sorted_err_list = logic_prep.sort_list_by_ele(err_list[idx], -1)
        logic.count_num_by_err(sorted_err_list)
        util.make_excel_err_list(WORK_DIR + "output/error_list_" + str(idx), sorted_err_list)





if __name__ == '__main__':
    start_time = time.perf_counter()
    print("start [ " + PROJECT_NAME + " ]>>>>>>>>>>>>>>>>>>")
    main()  # 1
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.perf_counter() - start_time))
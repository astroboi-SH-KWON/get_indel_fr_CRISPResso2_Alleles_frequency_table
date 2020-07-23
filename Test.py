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
FANCG = "AGAGGACAGTCAGCTCCAAG"
Trp53 = "TGCCATGGAGGAGTCACAGT"
POS_BRCD1_STRT = 0
POS_BRCD1_END = 9
GAP_ARR = [0, 1, 2, 3]
CONST1 = "AGTACGTACGAGTC"  # 14 bp
CONST2 = "GTACTCGCAGTAGTC"  # 15 bp

CONST_INIT = [POS_BRCD1_STRT, POS_BRCD1_END, GAP_ARR, CONST1, CONST2]

############### end setting env #################
def main():
    util = Util.Utils()
    logic_prep = LogicPrep.LogicPreps()

    brcd_list = util.csv_to_list_ignr_header(WORK_DIR + INPUT + BRCD_FILE)
    brcd_arr = logic_prep.make_arr_list_to_list(brcd_list)

    fancg_list = util.csv_to_list_ignr_header(WORK_DIR + INPUT + FANCG + F_TABLE_FILE, "\t")
    fancg_dict = logic_prep.get_data_by_cell_id(fancg_list, brcd_arr, CONST_INIT)





if __name__ == '__main__':
    start_time = time.perf_counter()
    print("start [" + PROJECT_NAME + "]>>>>>>>>>>>>>>>>>>")
    main()  # 1
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.perf_counter() - start_time))
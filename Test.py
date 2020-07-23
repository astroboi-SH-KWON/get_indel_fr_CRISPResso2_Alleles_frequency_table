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
FANCG = "AGAGGACAGTCAGCTCCAAG"
Trp53 = "TGCCATGGAGGAGTCACAGT"
POS_BRCD1_STRT = 0
POS_BRCD1_END = 9
GAP_ARR = [0, 1, 2, 3]
LEN_CONST1 = 14
LEN_BRCD2 = 9
LEN_CONST2 = 15

CONST_INIT = [POS_BRCD1_STRT, POS_BRCD1_END, GAP_ARR, LEN_CONST1, LEN_BRCD2, LEN_CONST2]

############### end setting env #################
def main():
    util = Util.Utils()

    fancg_list = util.csv_to_list_ignr_header(WORK_DIR + INPUT + FANCG + F_TABLE_FILE, "\t")
    print(fancg_list)



if __name__ == '__main__':
    start_time = time.perf_counter()
    print("start [" + PROJECT_NAME + "]>>>>>>>>>>>>>>>>>>")
    main()  # 1
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.perf_counter() - start_time))
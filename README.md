# get_indel_fr_CRISPResso2_Alleles_frequency_table
python3 Main.py

    2. analyze output file from 1. (./output/{guide_seq}/{fatq_1 fastq_2}/Alleles_frequency_table.txt)
        2-1 copy output files to input folder
        2-2 run Main.py
            python3 Main.py
    
    
    1. make 'Alleles_frequency_table.txt' by run_CRISPResso2_in_cmd
        input file : 
            ./input/var_list.txt
            ./FASTQ/[FASTQ files]
            
        python2 Multi_run_CRISPResso2.py
        
        output file :
            ./output/{guide_seq}/{fatq_1 fastq_2}/Alleles_frequency_table.txt
        

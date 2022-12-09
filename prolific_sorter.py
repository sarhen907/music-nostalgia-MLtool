
# Nostalgia Tool Survey  Quality Checker!! for prolific to easily give credit
# Sarah, December 2021

# This script scores from prolific-administered Qualtrics, using "numeric codes"

# two outputs:
# 1.  file with a list of the approved prolific IDs
# 2. Spreadsheet of everyone who was rejected and WHY

import os
import sys
import csv
import pandas as pd
import numpy as np
import glob
import math
import re
import datetime


import warnings
warnings.filterwarnings("ignore")


red = '\u001b[31m'
pink = '\u001b[35m'
yellow = '\u001b[33m'
green = '\u001b[32m'
blue = '\u001b[36m'
darkerblue = '\u001b[34;1m'

def score(log, outpath):

    outfilename_r = outpath + "/nostalgiatool_rejects.csv"
    outfilename_a = outpath + "/nostalgiatool_approves.csv"

    exists = os.path.isfile(outfilename_r)
    if exists:
        overwrite = input('stop! this file already exists! are you sure you want to overwrite? y or n: ')
        if overwrite == 'n':
            print('ok. quitting now.')
            return

    data = pd.read_csv(log)

    data.columns = data.columns.str.replace('.', '_')
    data.columns = data.columns.str.replace(' ', '_')
    data.columns = data.columns.str.replace("(","_")
    data.columns = data.columns.str.replace(")","_")



    colnames_r = ['id','reason']
    colnames_a = ['id']

    newdf_r = pd.DataFrame(columns = colnames_r, index = range(len(data)))
    newdf_a = pd.DataFrame(columns = colnames_a, index = range(len(data)))



    for index, row in data.iloc[2:].iterrows():
        if index > 367:
            reason = []
            print(green + "checking for quality...")

            if int(row.Progress) > 40:
                progressok =1


                if eval(row.Duration__in_seconds_)> 999:
                    timeok = 1
                else:
                    timeok = 0
                    reason.append('too_fast')
                    hold = 1

                at1 = 0
                at2 = 0
                at3 = 0
                if np.isnan(float(row.attention_question)) == 0:
                    if eval(row.attentioncheck1) == 2:
                        at1 = 1

                    if eval(row.attentioncheck2) == 4:
                        at2 = 1

                    if eval(row.attention_question) == 1:
                        at3 = 1

                listofshorts = 0

                if np.isnan(float(row.Q143_Page_Submit)) == 0:
                    if eval(row.Q143_Page_Submit) < 10:
                        listofshorts = listofshorts + 1
                if np.isnan(float(row.Q144_Page_Submit)) == 0:
                    if eval(row.Q144_Page_Submit) < 10:
                        listofshorts = listofshorts + 1
                if np.isnan(float(row.Q145_Page_Submit)) == 0:
                    if eval(row.Q145_Page_Submit) < 10:
                        listofshorts = listofshorts + 1
                if np.isnan(float(row.Q205_Page_Submit)) == 0:
                    if eval(row.Q205_Page_Submit) < 10:
                        listofshorts = listofshorts + 1
                if np.isnan(float(row.Q146_Page_Submit)) == 0:
                    if eval(row.Q146_Page_Submit) < 10:
                        listofshorts = listofshorts + 1
                if np.isnan(float(row.Q147_Page_Submit)) == 0:
                    if eval(row.Q147_Page_Submit) < 10:
                        listofshorts = listofshorts + 1
                if np.isnan(float(row.Q148_Page_Submit)) == 0:
                    if eval(row.Q148_Page_Submit) < 10:
                        listofshorts = listofshorts + 1
                if np.isnan(float(row.Q210_Page_Submit)) == 0:
                    if eval(row.Q210_Page_Submit) < 10:
                        listofshorts = listofshorts + 1
                if np.isnan(float(row.Q149_Page_Submit)) == 0:
                    if eval(row.Q149_Page_Submit) < 10:
                        listofshorts = listofshorts + 1
                if np.isnan(float(row.Q150_Page_Submit)) == 0:
                    if eval(row.Q150_Page_Submit) < 10:
                        listofshorts = listofshorts + 1
                if np.isnan(float(row.Q151_Page_Submit)) == 0:
                    if eval(row.Q151_Page_Submit) < 10:
                        listofshorts = listofshorts + 1
                if np.isnan(float(row.Q215_Page_Submit)) == 0:
                    if eval(row.Q215_Page_Submit) < 10:
                        listofshorts = listofshorts + 1

                if listofshorts < 4:
                    listeningok = 1
                else:
                    listeningok = 0

                    reason.append('listen_tooshort')


                if at1 == 0 or at2 == 0 or at3 ==0:

                    reason.append('attn_fail')



                if np.isnan(float(row.BANPS1_12)) == 0 and np.isnan(float(row.BANPS2_4)) == 0:
                    if eval(row.BANPS1_12) == eval(row.BANPS2_4):
                        banok = 0

                        reason.append('banps_fail')

                    else:
                        banok = 1
                else:
                    banok = 0

                if np.isnan(float(row.BANPS1_7)) == 0 and np.isnan(float(row.BANPS2_18)) == 0:
                    if eval(row.BANPS1_7) == eval(row.BANPS2_18):
                        ban1ok = 0

                        reason.append('banps_fail2')

                    else:
                        ban1ok = 1
                else:
                    ban1ok = 0

            else:
                progressok =0
                reason.append('no_finish')

            if progressok ==1 and timeok ==1 and at1 ==1 and at2 == 1 and at3==1 and listeningok == 1 and banok == 1 and ban1ok == 1:


                print(darkerblue+ 'Requirements met. adding participant to approve list ',index)

                newdf_a['id'][index] = row.PROLIFIC_PID

            else:
                print(red + "Requirement not met. moving on.")
                newdf_a = newdf_a.drop(index, axis=0)

                newdf_r['id'][index] = row.PROLIFIC_PID
                newdf_r['reason'][index] = reason

                continue


    newdf_r = newdf_r.dropna(axis=0, how='all')
    newdf_r.to_csv(outfilename_r,index =False)

    newdf_a = newdf_a.dropna(axis=0, how='all')
    newdf_a.to_csv(outfilename_a,index =False)
    print(yellow + "\n\nFull QC protocol complete.\n Goodbye!")
if __name__ == '__main__':
    try:
        score(*sys.argv[1:])
    except:
        print(red + "you have run this incorrectly!To run, type:\n \
        'python3.7 [name of script].py [full path of RAW DATA] [full path of output folder]'")

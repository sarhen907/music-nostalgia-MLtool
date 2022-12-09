

#this was created in 2021 to run for chords and lyrics analysis to fix any formatting issues with the chord copy and pasting
#Sarah Hennessy, 2021


import os
import sys
import csv
import pandas as pd
import numpy as np
import re


def score(datafolder, subject_outpath):

    subjectlist = [elem for elem in os.listdir(datafolder) if ".DS_Store" not in elem]

    print ('your txt list is:',subjectlist)

    subjectlist1 = [elem for elem in subjectlist if "chords" in elem]
    for subject in subjectlist1:

        subj = subject

        print("you are working on %s" %(subj))
        log = datafolder + "/%s" %(subject)
        print(log)
        data = pd.read_csv(log,skip_blank_lines=False)

        maxlen = data.shape[0]

        for index, row in data.iterrows():
            wrong = row.values
            mevfilename = subject_outpath + '/%s' %(subject)
            mevfile = open(mevfilename, 'a')

            if pd.isna(wrong) == 1:
                correct1 = ' '
            else:
                wrong = str(wrong)
                correct = re.sub(r"\s+", " ", wrong)
                correct1 = correct[2:-2]

            mevfile.write('%s\n' %(correct1))
            mevfile.close()

if __name__ == '__main__':
 try:
     score(*sys.argv[1:])
 except:
     print( "you have run this incorrectly!To run, type:\n \
     'python3.7 [name of script].py [full path of DATA FOLDER] [full path of OUTPUT folder]'")

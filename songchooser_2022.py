######### SONG CHOOSER SCRIPT ##########

# Nostalgia Tool Survey Scoring script
# Sarah, October 2021, updated December 2022

# This script scores from prolific-administered Qualtrics, using "numeric codes"
# output allows us to see which songs are control and unfamiliar
# It also retrieves names of songs from Spotify URI




import os
import sys
import csv
import pandas as pd
import numpy as np
import glob
import math
import re
import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = "ebde937b108d444cac9378e20cb1e681"
client_secret = "094131c3b42344808456d67e19885e89"


client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


import warnings
warnings.filterwarnings("ignore")


red = '\u001b[31m'
pink = '\u001b[35m'
yellow = '\u001b[33m'
green = '\u001b[32m'
blue = '\u001b[36m'
darkerblue = '\u001b[34;1m'


backscore_4pt = {1:4,2:3,3:2,4:1}
backscore_5pt = {1:5,2:4,3:3,4:2,5:1}
backscore_7pt= {1:7,2:6,3:5,4:4,5:3,6:2,7:1}

def score(log,outpath):

    def substring_after(s, delim):
        return s.partition(delim)[2]

    outfilename = outpath + "/nostalgiatool_fMRI_songChooser.csv"
    cleanname = outpath + "/nostalgia_clean.csv"

    exists = os.path.isfile(outfilename)
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


    colnames = ['id','c_which','u_which','N1_artist','N1_song','N2_artist','N2_song','N3_artist','N3_song','N4_artist','N4_song','N5_artist','N5_song','N6_artist','N6_song', 'C1_artist','C1_song','C2_artist','C2_song','C3_artist','C3_song','C4_artist','C4_song','C5_artist','C5_song','C6_artist','C6_song','U1_artist','U1_song','U2_artist','U2_song','U3_artist','U3_song',\
    'U4_artist','U4_song','U5_artist','U5_song','U6_artist','U6_song', 'N1_name','N2_name','N3_name','N4_name','N5_name','N6_name', 'C1_name','C2_name','C3_name','C4_name','C5_name','C6_name','U1_name','U2_name','U3_name',\
    'U4_name','U5_name','U6_name', 'N1_nost','N2_nost','N3_nost','N4_nost','N5_nost','N6_nost']



    newdf = pd.DataFrame(columns = colnames, index = range(len(data)))



    for index, row in data.iloc[2:].iterrows():
        #if ExternalReference startswith
        id = data['ExternalReference'][index]
        print(id)
        newdf['id'][index] = id

        if pd.isnull(id) == 0:
            progressok = 1
            #print('ok')
        else:
            progressok = 0
            print('skipping...')


        if progressok == 1:
            print(darkerblue+ 'Requirements met. Scoring for this participant: ',index)

            accuracylist = []

            c_which =[]
            u_which = []


            for i in range(1,7):
                for j in range(1,11):
                    convertme = data['C%d_%d_fam' %(i,j)][index]
                    data['C%d_%d_fam' %(i,j)][index]= pd.to_numeric(convertme)

            for i in range(1,7):

                bad_reasons = []
                achieved = 0
                uachieved =0

                for j in range(1,11):

                    if ((math.isnan(data['C%d_%d_fam' %(i,j)][index])) == 0) and ((data['C%d_%d_fam' %(i,j)][index]) > 1):

                        if int(data['C%d_%d_nost' %(i,j)][index]) < 5:
                            if achieved ==0:
                                c_which.append(j)
                                achieved = 1
                        else:
                            bad_reasons.append('toonost')
                    elif ((data['C%d_%d_fam' %(i,j)][index]) == 1):
                        #print("this could be a nice unfam song\n")
                        bad_reasons.append('nofam')
                        if uachieved == 0:
                            u_which.append(j)
                            uachieved = 1


                    if (j == 10) and achieved == 0:
                        c_which.append(0)

                    if (j==10) and uachieved == 0:
                        u_which.append(0)

            newdf['c_which'][index]= c_which

            newdf['u_which'][index]= u_which

            newdf['N1_name'][index]=row.shortUri1
            newdf['N2_name'][index]=row.shortUri2
            newdf['N3_name'][index]=row.shortUri3
            newdf['N4_name'][index]=row.shortUri4
            newdf['N5_name'][index]=row.shortUri5
            newdf['N6_name'][index]=row.shortUri6

            newdf['N1_nost'][index]=row.N1_nost
            newdf['N2_nost'][index]=row.N2_nost
            newdf['N3_nost'][index]=row.N3_nost
            newdf['N4_nost'][index]=row.N4_nost
            newdf['N5_nost'][index]=row.N5_nost
            newdf['N6_nost'][index]=row.N6_nost


            for i in range(0, 6):
                print(i+1)

                N_name = data['shortUri%d'%(i+1)][index]

                uri = substring_after(N_name,'https://open.spotify.com/embed/track/')
                track = sp.track(uri)

                artists = track['artists']
                artistName = artists[0].get('name')
                print(pink + "ARTISTNAME")
                print(artistName)
                newdf['N%d_artist'%(i+1)][index] = artistName

                #get songName
                name = track['name']
                print(pink + "TRACK NAME:")
                print(name)
                newdf['N%d_song'%(i+1)][index] = name


            for i in range(0, len(c_which)):
                if int(c_which[i]) != 0:
                    C_name = data['rec%d%d' %(i+1,c_which[i])][index]
                    newdf['C%d_name' %(i+1)][index]= C_name


                    if C_name.startswith('http')== True:
                        uri = substring_after(C_name,'https://open.spotify.com/embed/track/')
                        track = sp.track(uri)

                        artists = track['artists']
                        artistName = artists[0].get('name')
                        print(pink + "ARTISTNAME")
                        print(artistName)
                        newdf['C%d_artist'%(i+1)][index] = artistName

                        #get songName
                        name = track['name']
                        print(pink + "TRACK NAME:")
                        print(name)
                        newdf['C%d_song'%(i+1)][index] = name

                else:
                    C_name = ''
                    newdf['C%d_name' %(i+1)][index] = C_name

            for i in range(0, len(u_which)):

                if u_which[i] != 0:
                    U_name =  data['rec%d%d' %(i+1,u_which[i])][index]
                    newdf['U%d_name' %(i+1)][index]= U_name

                else:
                    U_name = ''
                    newdf['U%d_name' %(i+1)][index] = U_name


        else:
            print(red + "Requirement not met. moving on.")
            newdf = newdf.drop(index, axis=0)
            continue


    newdf = newdf.dropna(axis=0, how='all')
    newdf.to_csv(outfilename,index =False)
    print(yellow + "\n\nFull scoring protocol complete.\n Goodbye!")
if __name__ == '__main__':
    try:
        score(*sys.argv[1:])
    except:
        print(red + "you have run this incorrectly!To run, type:\n \
        'python3.7 [name of script].py [full path of RAW DATA] [full path of output folder]'")

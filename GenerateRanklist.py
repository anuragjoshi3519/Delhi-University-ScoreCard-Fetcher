import os
import pandas as pd
from bs4 import BeautifulSoup
from Utility import fetchGradeCard, isResultOut

def generateRanks(clgCode, rollNoList):
    
    flag = False
    sem = None
    course = None
    invalids = []
    rankData = {'Exam Roll Number':[], 'Name':[], 'CGPA':[]}
    
    for rollNo in rollNoList:
        ret = fetchGradeCard(clgCode, rollNo, False)
        
        if ret == 0 or ret == 1:
            invalids.append(rollNo)
            #print(f'{rollNo} is an invalid exam roll number. Skipping..')
            continue

        soup = BeautifulSoup(open(f'.temp/{rollNo}.html'), "html.parser")

        if flag==False:
            course = soup.find('span', {'id':'lblcourse'}).text
            sem = soup.find('span', {'id':'lblsem'}).text
            #clgName = soup.find('span', {'id':'lblcollege'}).text
            flag=True
            
        rankData['Exam Roll Number'].append(soup.find('span', {'id':'lblrollno'}).text)
        rankData['Name'].append(soup.find('span', {'id':'lblname'}).text)
        tr = soup.find('table',{"id":"gv_sgpa"}).find_all('td')

        tr = tr[-6:]

        rankData['CGPA'].append(float(tr[3].text))

    if len(invalids) == len(rollNoList):
        return 'Sorry! Results are not out yet.\n'

    else:
        rankDF = pd.DataFrame(rankData)
        rankDF.sort_values(by=["CGPA"],ascending=False,kind="mergesort",inplace=True)
        rankDF.reset_index(drop=True, inplace=True)
        rankDF.index = [*range(1,len(rankData['Name'])+1)]
        rankDF['Rank'] = rankDF['CGPA'].rank(ascending=False,method="dense").astype(int)

        if not os.path.isdir('RankLists'):
            os.mkdir('RankLists')

        rankDF.to_csv(f'RankLists/{course}_{sem}.csv',index=False)

        return "Rank list has been successfully generated and saved in 'RankLists' folder"

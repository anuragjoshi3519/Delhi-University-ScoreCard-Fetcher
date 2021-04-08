import os
import glob
import time
from SendMail import sendMail
from config import URL,HEADER
from GenerateRanklist import *
from Utility import fetchGradeCard, isResultOut, getClgCodes

def downloadAllResult(clgCode, rollNoList):
    invalids = []
    
    for rollNo in rollNoList:
        ret = fetchGradeCard(clgCode, str(rollNo))
        if ret == 0 or ret == 1:
            invalids.append(rollNo)
            #print(f'{rollNo} is not a valid exam roll number. Skipping..')
            continue
    if len(invalids) == len(rollNoList):
        return 'Sorry! Results are not out yet.\n' 
    else:
        return "Result PDFs  has been successfully generated and saved in 'Result-PDFs' folder"
            
def getResult(subject, sem, clgCode, rollNo, email_to):
        
    while True:
        if isResultOut(subject,sem):

            filepath = fetchGradeCard(clgCode, rollNo)

            if filepath==1:
                print('Sorry, No record found in database. Please try again later.')
            elif filepath!=0 and email_to!='':
                sendMail(email_to, filepath) 
            elif filepath!=0 and email_to=='':
                print("Your result pdf is saved in 'Results_pdf' folder ")
            else:
                print('Error in fetching result.')
            break
        else:
            time.sleep(1200)

            
def getCollegeCode():
    
    clgCode = None
    while True:
        clgCode = input("\nEnter College Code : ")
        if clgCode in getClgCodes():
            break
        else:
            print('Please enter a valid college code.')
    return clgCode

def getSubjectAndSem():
    
    subject = input("\nEnter Course Name : ").lower()
    sem = None
    while True:
        try:
            sem = sem_encodings[int(input("\nEnter Semester: "))]
            break
        except:
            print('Please enter in range (1-6). Try again.')
    return subject,sem


def main():
    
    sem_encodings={1:'I',2:'II',3:'III',4:'IV',5:'V',6:'VI'}
    
    choice = input("\n'A' : Fetch your result.\n'B' : Fetch multiple results. \n'C' : Generate rank list. \n\n(Enter any other key to exit.): ")
    
    if choice.lower()=='a':
        
        subject = ''
        sem = ''
        email_to = ''
        clgCode = getCollegeCode()
        
        keep_running = input("\nKeep this script running until your result is declared and mailed to you? (Y/[n]): ")
        
        if keep_running.lower()=='y':
            subject, sem = getSubjectAndSem()
        
        rollNo = input("\nEnter roll no.: ")
        
        if keep_running.lower()=='y':
            choiceMail = 'y'
        else:
            choiceMail = input("\nEmail result pdf? (Y/n): ")
            
        print("\n\nProcessing...\n")
        
        if choiceMail.lower() == 'y':
            email_to = input("\nEnter recipient's email id: ")
        
        getResult(subject, sem, clgCode, rollNo, email_to)
        
    elif choice.lower()=='b' or choice.lower()=='c':
        
        start = None
        end = None
        clgCode = getCollegeCode()
        
        while True:
            start = int(input("\nEnter starting roll no.: "))
            end = int(input("\nEnter ending roll no.: "))
            
            if start>end or end-start>200:
                print("\nInvalid input. Please try again.")
                continue
            break
                
        rollNumberList = list(map(str,[*range(start,end+1)]))
        
        print("\n\nProcessing...\n")
        
        
        if choice.lower()=='b':
            message = downloadAllResult(clgCode, rollNumberList)
        else:
            message = generateRanks(clgCode, rollNumberList)
            
        print(message)
        
    else:
        return 0
    
    files = glob.glob('.temp/*')
    for f in files:
        os.remove(f)
        
    if os.path.isdir('.temp'):
        os.rmdir('.temp/')
    
    print('\nDone')

if __name__=='__main__':
    
    print("\n\nTo check your college code, run: $ python3 printClgCodes.py")
    print("------------------------------------------------------------\n")
    
    main()

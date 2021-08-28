import os
import glob
import time
import getpass
from SendMail import sendMail, sendMailSMTP
from config import URL,HEADER
from GenerateRanklist import *
from Utility import fetchGradeCard, isResultOut, getClgCodes, printClgCodes, printCourseNames

def downloadAllResult(clgCode, rolldobList):
    invalids = []
    
    for rollNo,dob in rolldobList:
        ret = fetchGradeCard(clgCode, str(rollNo), dob[0], dob[1], dob[2])
        if ret == 0 or ret == 1:
            invalids.append(rollNo)
            #print(f'{rollNo} is not a valid exam roll number. Skipping..')
            continue
    if len(invalids) == len(rolldobList):
        return 'Sorry! Results are not out yet.\n' 
    else:
        return "Result PDFs  has been successfully generated and saved in 'Downloads/' folder"
            
def getResult(subject, sem, clgCode, rollNo, email_from, email_pass, email_to, dd, mm, yyyy):
        
    while True:
        if isResultOut(subject,sem):

            filepath = fetchGradeCard(clgCode, rollNo, dd, mm, yyyy)

            if filepath==1:
                print('Sorry, No record found in database. Please try again later.')
            elif filepath!=0 and email_to!='':
                sendMailSMTP(email_from, email_pass, email_to, filepath)
            elif filepath!=0 and email_to=='':
                print("Your result pdf is saved in 'Downloads/' folder ")
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

def getSemester():
    
    sem_encodings={1:'I',2:'II',3:'III',4:'IV',5:'V',6:'VI'}
    sem = None
    while True:
        try:
            sem = sem_encodings[int(input("\nEnter Semester: "))]
            break
        except:
            print('Please enter in range (1-6). Try again.')
    return sem


def main():
    try:
        os.system('clear')
    except:
        pass
    
    choice = input("Welcome to AutoFetch Service\n----------------------------\n\nA : Fetch your result.\nB : Fetch multiple results. \nC : Generate rank list. \n\nX : Print all college codes. \nY : Print all course names. \n\n(Enter any other key to exit): ")
    
    if choice.lower()=='x':
        printClgCodes()
        input("\nPress Enter key to continue ")
        try:
            os.system('clear')
        except:
            pass
        main()
        
    if choice.lower()=='y':
        printCourseNames()
        input("\nPress Enter key to continue ")
        try:
            os.system('clear')
        except:
            pass
        main()
        
    if choice.lower()=='a':
        
        subject = ''
        sem = ''
        email_from = ''
        email_pass = ''
        email_to = ''
        clgCode = getCollegeCode()
        
        keep_running = input("\nKeep this script running until your result is declared and mailed to you? (Y/[n]): ")
        
        if keep_running.lower()=='y':
            subject = input("\nEnter Course Name : ").lower()
            sem = getSemester()
        
        rollNo = input("\nEnter roll no.: ")
        dob = input("\nEnter DOB (dd-mm-yyyy): ")
        dd, mm, yyyy = tuple(map(int,dob.split('-')))
        
        if keep_running.lower()=='y':
            choiceMail = 'y'
        else:
            choiceMail = input("\nEmail result pdf? (Y/n): ")
                    
        if choiceMail.lower() == 'y':
            print("\nNote: Make sure to allow 'less secure apps' in your gmail account to use email services (refer to link in readme.md file)")
            email_from = input("\nEnter sender's gmail id: ")
            email_pass = getpass.getpass("Enter your password: ")
            email_to = input("\nEnter recipient's email id: ")

        print("\nProcessing...")

        getResult(subject, sem, clgCode, rollNo, email_from, email_pass, email_to, dd, mm, yyyy)
        
    elif choice.lower()=='b' or choice.lower()=='c':
        
        n = int(input("\nEnter total number of students: "))
        rolldobList = []
        clgCode = getCollegeCode()
        
        for i in range(1,n+1): 
            rollNo = input(f"\nStudent #{i} Roll no. :")
            dob = input(f"Student #{i} DOB (dd-mm-yyyy): ")
            dob = list(map(int,dob.split('-')))
            rolldobList.append((rollNo,dob))
        
        print("\nProcessing...")
        
        
        if choice.lower()=='b':
            message = downloadAllResult(clgCode, rolldobList)
        else:
            message = generateRanks(clgCode, rolldobList)
            
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
    main()

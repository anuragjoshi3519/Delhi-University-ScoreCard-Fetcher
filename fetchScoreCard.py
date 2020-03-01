import time
import os
import getpass

from SendMail import sendMail
from Utility import printClgCodes, connect, fetchGradeCard, isResultOut, getClgCodes

def downloadAllResult(subject,sem, clgCode, rollNoList):
    
    while True:
        if isResultOut(subject,sem):
        
            for rollNo in rollNoList:
                _ = fetchGradeCard(clgCode, str(rollNo))

            break
            
        else:
            time.sleep(60)
            
def getResult(subject, sem, clgCode, rollNo, email_from='', email_pass='', email_to=''):
        
    while True:
        if isResultOut(subject,sem):
            
            filepath = fetchGradeCard(clgCode, rollNo)

            if filepath==1:
                print('Your result is not out yet.')
            elif filepath!=0 and email_from!='':
                sendMail(email_from, email_pass, email_to, filepath) 
            elif filepath!=0 and email_from=='':
                print("Your result pdf is saved in 'Results_pdf' folder ")
            else:
                print('Error in fetching result.')
            
            break
        else:
            time.sleep(60)  
            
def main():

    keep_running = input("Keep this script running until your result is declared and mailed to you? (Y/n): ")

    sem_encodings={1:'I',2:'II',3:'III',4:'IV',5:'V',6:'VI'}
    
    if keep_running.lower()=='y':
        subject = input("\nEnter Course Name : ").lower()
    else:
        subject=''
        
    while True:
        try:
            sem = sem_encodings[int(input("\nEnter Semester: "))]
            break
        except:
            print('Please enter in range (1-6). Try again.')
            continue

    while True:
        clgCode = input("\nEnter College Code : ")
        if clgCode in getClgCodes():
            break
        else:
            print('Please enter a valid college code.') 
    
    choice = input("\nEnter 'A': To fetch your result.\nEnter 'B': To fetch multiple results. \n(Enter any other key to exit.): ")
    
    if choice.lower()=='a':
        
        rollNo = input("\nEnter roll no.: ")
        
        if keep_running.lower()=='y':
            choiceMail = 'y'
        else:
            choiceMail = input("\nEmail result pdf? (Y/n): ")
            
        if choiceMail.lower() == 'y':
            email_from = input("\nEnter your mail id: ")
            email_pass = getpass.getpass("\nEnter your password: ")
            email_to = input("\nEnter recipient mail id: ")
            
            print("\n\nProcessing...\n")
            getResult(subject, sem, clgCode, rollNo, email_from, email_pass, email_to)
        else:
            print("\n\nProcessing...\n")
            getResult(subject, sem, clgCode, rollNo)
        
        print('Done')
        
    elif choice.lower()=='b':
        start = int(input("\nEnter starting roll no.: "))
        end = int(input("\nEnter ending roll no.: "))
        
        print("\n\nProcessing...\n")
        downloadAllResult(subject, sem, clgCode, list(range(start,end+1)) )
        
        print('Done')
    else:
        return 0

if __name__=='__main__':
    
    print("\nYou can check your college code by running the command: $ python printClgCodes.py ")
    print("----------------------------------------------------------------------------------")
    print("----------------------------------------------------------------------------------\n")
    
    main()

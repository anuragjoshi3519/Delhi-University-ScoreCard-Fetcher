import time
import os
import getpass

from SendMail import sendMail
from Utility import printClgCodes, connect, fetchGradeCard, isResultOut

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
    #os.mkdir('Results_pdf')
    #os.mkdir('data')
    
    keep_running = input("Keep this script running until your result is declared and mailed to you? (Y/n): ")

    sem_encodings={1:'I',2:'II',3:'III',4:'IV',5:'V',6:'VI'}
    
    if keep_running=='y':
        subject = input("\n\nEnter Course Name : ")
    else:
        subject=''
        
    while True:
        try:
            sem = sem_encodings[int(input("\nEnter Semester: "))]
            break
        except:
            print('Please enter in range (1-6). Try again.')
            continue

    clgCode = input("Enter College Code : ")
    choice = input("Enter 'A': To fetch your result.\nEnter 'B': To fetch multiple results. \n(Enter any other key to exit.): ")
    
    if choice.lower()=='a':
        
        rollNo = input("Enter roll no.: ")
        
        if keep_running=='y':
            choiceMail = 'y'
        else:
            choiceMail = input("Email result pdf? (Y/n): ")
            
        if choiceMail.lower() == 'y':
            email_from = input("Enter your mail id: ")
            email_pass = getpass.getpass("Enter your password: ")
            email_to = input("Enter recipient mail id: ")
            
            print("\n\nProcessing...\n")
            getResult(subject, sem, clgCode, rollNo, email_from, email_pass, email_to)
        else:
            print("\n\nProcessing...\n")
            getResult(subject, sem, clgCode, rollNo)
        
        print('Done')
        
    elif choice.lower()=='b':
        start = int(input("Enter starting roll no.: "))
        end = int(input("Enter ending roll no.: "))
        
        print("\n\nProcessing...\n")
        downloadAllResult(subject, sem, clgCode, list(range(start,end+1)) )
        
        print('Done')
    else:
        return 0

if __name__=='__main__':
    
    print("You can check your college code by running the command: $ python printClgCodes.py ")
    print("----------------------------------------------------------------------------------")
    print("----------------------------------------------------------------------------------\n")
    
    main()

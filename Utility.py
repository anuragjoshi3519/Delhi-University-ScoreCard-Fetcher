import re
import requests
import urllib.request
from PIL import Image
import pytesseract
import pdfkit
import os
import pickle
from bs4 import BeautifulSoup
from config import URL,HEADER

def connect():
    
    if not os.path.isdir('data'):
        os.mkdir('data')
        
    with requests.Session() as request:

        form_data={}
        
        try:
            response = request.get(URL,headers=HEADER)
            soup = BeautifulSoup(response.text,'html.parser')

            #Bypassing Captcha
            #-----------------
            for link in soup.find_all('img' ,  {'id': 'imgCaptcha'}):
                captcha = link.get('src')

            captchaLink = URL.split('Combine_GradeCard.aspx')[0]+captcha
            urllib.request.urlretrieve(captchaLink,'data/captcha.jpg')
            captchaText = pytesseract.image_to_string(Image.open('data/captcha.jpg'))
            #-----------------

            viewstate = soup.select("#__VIEWSTATE")[0]['value']
            eventValidation = soup.select("#__EVENTVALIDATION")[0]['value']
            viewstateGenerator = soup.select('#__VIEWSTATEGENERATOR')[0]['value']

            form_data={
                '__EVENTTARGET':'', 
                '__EVENTARGUMENT':'', 
                '__VIEWSTATE': viewstate,
                '__VIEWSTATEGENERATOR': viewstateGenerator,
                '__EVENTVALIDATION': eventValidation,
                'txtcaptcha': captchaText,
                'btnsearch': 'Print Score Card'
               }
        except:
            return form_data
        
    return form_data  


def fetchGradeCard(clgCode,rollno):
    
    form_data = connect()
    if len(form_data)==0:
        return 0
    form_data['ddlcollege']=str(clgCode)
    form_data['txtrollno']=str(rollno)
    
    try:
        
        result = requests.post(URL, data=form_data,headers=HEADER)
        result = BeautifulSoup(result.text,'html.parser')
         
        while len(result.body.findAll(text=re.compile('^Sorry! Invalid captch code.$')))!=0:
            form_data = connect()
            form_data['ddlcollege']=str(clgCode)
            form_data['txtrollno']=str(rollno)
            result = requests.post(URL, data=form_data,headers=HEADER)
            result = BeautifulSoup(result.text,'html.parser')
            
        if len(result.body.findAll(text=re.compile('^Sorry! no record found.$')))!=0: 
            return 1
        
        for img in result.findAll('img'):
            img.decompose()
            
        if not os.path.isdir('Result-PDFs'):
            os.mkdir('Result-PDFs')

        filepath = 'Result-PDFs/ScoreCard_'+rollno+'.pdf'

        with open('data/page.html','w',encoding='utf-8') as f:
            f.write(str(result))

        options = {
            'quiet': '',
            'encoding': "UTF-8",
            'print-media-type': '',
            'page-size': 'A4',
            'margin-top': '5mm',
            'margin-bottom': '5mm',
            'margin-left': '5mm',
            'margin-right': '5mm',
            'zoom': '1.5'
        }
        pdfkit.from_file('data/page.html',filepath,options=options)
        
    except:
        return 0
    
    return filepath

def isResultOut(courseName, sem):
    try:
        response = requests.get(URL.split('Combine_GradeCard.aspx')[0]+'List_Of_Declared_Results.aspx',headers=HEADER)
        soup = BeautifulSoup(response.text,'html.parser')
        cells = soup.find('table',attrs={'id':"gvshow_Reg"}).findAll('td')[2:]
        courseName = ''.join([s for s in courseName if s.isalnum()])
        
        course = []
        semester = []
        for i in range(1,len(cells),6):
            course.append(''.join([s for s in cells[i].text.lower() if s.isalnum()]))
            semester.append(cells[i+2].text)
    
        course_sem_dict = dict(zip(course,semester))    

        if courseName!='':
            flag=0
            for course,semester in course_sem_dict.items():
                if (courseName.lower() in course) and (sem.lower() == semester.lower()) :
                    flag=1
            if flag==1:
                return True
            else:
                return False
        return True
    
    except:
        
        #print('Error occurred in fetching result. Retrying...')
        return False

def getCoursesNames():
    try:
        response = requests.get(URL.split('Combine_GradeCard.aspx')[0]+'List_Of_Declared_Results.aspx',headers=HEADER)
        soup = BeautifulSoup(response.text,'html.parser')
        cells = soup.find('table',attrs={'id':"gvshow_Reg"}).findAll('td')[2:]

        courses = []
        for i in range(1,len(cells),6):
            courses.append(''.join([s for s in cells[i].text]))
        courses = sorted(set(courses))
        
        with open('Resources/CoursesNames.txt','w') as f:
            for i,name in enumerate(courses):
                f.write(f'{i+1}) {name}\n')
    
    except:
        #print('Error in fetching Course names.')
        return False

def fetchAndSaveClgCodes():
    try:
        response = requests.get(URL,headers=HEADER)
        soup = BeautifulSoup(response.text,'html.parser')

        s=soup.find('select',{'id':'ddlcollege'})
        items=s.find_all('option')[1:]
        clgCode = [item.get('value') for item in items]
        clgName = [item.text for item in items]

        clgCodeDict = dict(zip(clgName,clgCode))
        with open('Resources/collegeCodes.pkl','wb') as f:
            pickle.dump(clgCodesDict,f)
    
    except:
        #print('Error in fetching!')
        return {}

    return clgCodeDict    

def getClgCodes():
    
    with open('Resources/collegeCodes','rb') as g:
        clgCodeList = pickle.load(g)
        
    return list(clgCodeList.values())   

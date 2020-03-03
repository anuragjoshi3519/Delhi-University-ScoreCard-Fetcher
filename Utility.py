import re
import requests
import urllib.request
from PIL import Image
import pytesseract
import pdfkit
import os
from bs4 import BeautifulSoup


def connect():
    url = 'https://duresult.in/students/Combine_GradeCard.aspx'
    header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

    if not os.path.isdir('data'):
        os.mkdir('data')
    with requests.Session() as request:

        form_data={}
        
        try:
            response = request.get(url,headers=header)
            soup = BeautifulSoup(response.text,'html.parser')

            #Bypassing Captcha
            #-----------------
            for link in soup.find_all('img' ,  {'id': 'imgCaptcha'}):
                captcha = link.get('src')

            captchaLink = 'https://duresult.in/students/'+captcha
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
            pass
        
    return form_data  


def fetchGradeCard(clgCode,rollno):

    url = 'https://duresult.in/students/Combine_GradeCard.aspx'
    header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

    form_data = connect()
    form_data['ddlcollege']=str(clgCode)
    form_data['txtrollno']=str(rollno)
    
    try:
        
        result = requests.post(url, data=form_data,headers=header)
        result = BeautifulSoup(result.text,'html.parser')
         
        while len(result.body.findAll(text=re.compile('^Sorry! Invalid captch code.$')))!=0:
            form_data = connect()
            form_data['ddlcollege']=str(clgCode)
            form_data['txtrollno']=str(rollno)
            result = requests.post(url, data=form_data,headers=header)
            result = BeautifulSoup(result.text,'html.parser')
            
        if len(result.body.findAll(text=re.compile('^Sorry! no record found.$')))!=0: 
            return 1
        
        for img in result.findAll('img'):
            img.decompose()
            
        if not os.path.isdir('Results_pdf'):
            os.mkdir('Results_pdf')

        filepath = 'Results_pdf/ScoreCard_'+rollno+'.pdf'

        with open('data/page.html','w') as f:
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

def isResultOut(subject, sem):
    try:
        url='https://duresult.in/students/List_Of_Declared_Results.aspx'
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.text,'html.parser')
        cells = soup.find('table',attrs={'id':"gvshow_Reg"}).findAll('td')[2:]
        
        subject = ''.join([s for s in subject if s.isalnum()])

        course = []
        semester = []
        for i in range(1,len(cells),6):
            course.append(''.join([s for s in cells[i].text.lower() if s.isalnum()]))
            semester.append(cells[i+2].text)  
    
        course_sem_dict = dict(zip(course,semester))    

        for course,semester in course_sem_dict.items():
            if (subject in course) and (semester.lower()==sem.lower()) :
                return True
    except:
        
        #print('Error occurred in fetching result. Retrying...')
        return False

    return False


def printClgCodes():
    url = 'https://duresult.in/students/Combine_GradeCard.aspx'
    header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

    try:
        response = requests.get(url,headers=header)
        soup = BeautifulSoup(response.text,'html.parser')

        s=soup.find('select',{'id':'ddlcollege'})
        items=s.find_all('option')[1:]
        clgCode = [item.get('value') for item in items]
        clgName = [item.text for item in items]

        clgCodeList = dict(zip(clgName,clgCode))

        for clg,code in clgCodeList.items():
            print('{} -- {}'.format(clg,code))
    
    except:
        print('Error in printing!')

def getClgCodes():
    
    url = 'https://duresult.in/students/Combine_GradeCard.aspx'
    header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

    try:
        response = requests.get(url,headers=header)
        soup = BeautifulSoup(response.text,'html.parser')

        s=soup.find('select',{'id':'ddlcollege'})
        items=s.find_all('option')[1:]
        clgCode = [item.get('value') for item in items]
        return clgCode
    
    except:
        print('Error!')

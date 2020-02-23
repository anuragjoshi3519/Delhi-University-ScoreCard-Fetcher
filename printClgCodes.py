from bs4 import BeautifulSoup
import requests

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
        
if __name__=='__main__':
    printClgCodes()

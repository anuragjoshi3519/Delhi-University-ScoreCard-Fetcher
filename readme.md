## First run the following commands on terminal to install required packages : 

* sudo apt-get update && sudo apt-get upgrade
* sudo wget https://builds.wkhtmltopdf.org/0.12.1.3/wkhtmltox_0.12.1.3-1~bionic_amd64.deb
* sudo dpkg -i wkhtmltox_0.12.1.3-1~bionic_amd64.deb
* sudo apt-get install -f
* sudo ln -s /usr/local/bin/wkhtmltopdf /usr/bin
* sudo apt-get install tesseract-ocr && sudo apt-get install libtesseract-dev && sudo apt-get install python-lxml

* sudo apt-get install python3-pip
* pip3 install pdfkit
* pip3 install pytesseract
* pip3 install requests
* pip3 install bs4
* pip3 install Pillow
* pip3 install lxml
* pip3 install email


_# make sure you have python3.x and pip installed on your system_

## To run the program:

1. First clone the repository
2. Using terminal, head the cloned folder

   _You should know your college code, roll number, and course name (optional) to successfully fetch results_ 
3. Check your college code by running:- $ python3 printClgCodes.py
4. Run 'fetchScoreCard.py' and start fetching:- $ python3 fetchScoreCard.py




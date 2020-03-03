## First run the following commands on terminal to install required packages : 

1. sudo apt-get update
2. sudo wget https://builds.wkhtmltopdf.org/0.12.1.3/wkhtmltox_0.12.1.3-1~bionic_amd64.deb
3. sudo dpkg -i wkhtmltox_0.12.1.3-1~bionic_amd64.deb
4. sudo apt-get install -f
5. sudo apt-get install tesseract-ocr && sudo apt-get install libtesseract-dev
6. sudo apt-get install python3-pip
7. pip install -r requirements.txt

_# make sure you have python3.x installed on your system_

## To run the program:

1. First clone the repository
2. Using terminal, head the cloned folder

   _You should know your college code, roll number, and course name (optional) to successfully fetch results_ 
3. Check your college code by running:- $ python3 printClgCodes.py
4. Run the program and start fetching:- $ python3 fetchScoreCard.py

*_Make sure to allow gmail [less secure apps](https://myaccount.google.com/lesssecureapps) to use email services._*




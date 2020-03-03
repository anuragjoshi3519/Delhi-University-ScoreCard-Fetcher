## About

Are you tired of waiting and checking if your semesters' results are out? :hourglass_flowing_sand: :disappointed_relieved:

No need to do any of that now. Just run a single python script and relax. :relieved:

The script will do all the necessary things to make sure your result is e-mailed to you as soon as it declares. :heavy_check_mark:

## Features

1. DU ScoreCard Fetcher can be used for fetching single as well as multiple result scorecards PDF.
2. Any student belonging to any course or any college in Delhi University can use it to fetch results. 
3. You can opt to get your result PDF downloaded in your system and by email too.
4. You can even keep the script running, in your local or remote server, until the results are out (and you will be notified by an email once they are out )

## How to use?

### First run the following commands on terminal to install required packages : 

1. sudo apt-get update
2. sudo wget https://builds.wkhtmltopdf.org/0.12.1.3/wkhtmltox_0.12.1.3-1~bionic_amd64.deb
3. sudo dpkg -i wkhtmltox_0.12.1.3-1~bionic_amd64.deb
4. sudo apt-get install -f
5. sudo apt-get install tesseract-ocr && sudo apt-get install libtesseract-dev
6. sudo apt-get install python3-pip

_Make sure you have python3.x installed on your system_

### Now to run the program:

1. First clone the repository
2. Using terminal, go the cloned folder

   _You should know your college code, roll number, and course name (optional) to successfully fetch results_ 
3. Run:-  *pip3 install -r requirements.txt*
4. Check your college code by running:-  *python3 printClgCodes.py*
5. Run this script and start fetching:-  *python3 fetchScoreCard.py*

_Make sure to allow gmail [less secure apps](https://myaccount.google.com/lesssecureapps) to use email services._




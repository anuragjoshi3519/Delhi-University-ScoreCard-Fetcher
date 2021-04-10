## About

Are you tired of waiting and checking if your semesters' results are out? :hourglass_flowing_sand:  
No need to do any of that now. Just run a single python script and relax. :relieved:  
The script will do all the necessary things to make sure your result is e-mailed to you as soon as it declares. :heavy_check_mark:

## Features

* DU ScoreCard Fetcher can be used for fetching single as well as multiple result scorecards PDF.
* You can choose to get your result PDF downloaded in your system as well as by email.
* You can generate class wide rank lists for any course.
* You can even keep the script running, in your local or remote server, until the results are out (and you will be notified by an email once they are out )
* Any student belonging to any course or any college in Delhi University can use it to fetch his/her result PDF.

## How to use?

### First run the following commands on terminal to install required packages : 

<!--- wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.deb --->
<!--- sudo dpkg -i wkhtmltox_0.12.6-1.bionic_amd64.deb --->
<!--- sudo apt-get install -f --->

```bash
sudo apt-get update
sudo apt-get install wkhtmltopdf
sudo apt-get --fix-broken install
sudo apt-get install tesseract-ocr && sudo apt-get install libtesseract-dev
sudo apt-get install python3-pip && sudo apt-get install python3-venv
```

>Make sure you have python3.x installed on your system

### Now to start using the fetcher, first run:

```bash
git clone https://github.com/anuragjoshi3519/Delhi-University-ScoreCard-Fetcher.git
cd Delhi-University-ScoreCard-Fetcher
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

**Now the setup is complete. To start fetching, run:**
 
 ```bash
 python3 fetchScoreCard.py
 ```


<!-- **NOTE :** -->

<!-- >Make sure to allow gmail [less secure apps](https://myaccount.google.com/lesssecureapps) to use email services. -->



**Few utility python scripts:**

1. To check all **college codes**, run :-  `python3 printClgCodes.py` 
2. To check all **courses names**, run :-  `python3 printCourseNames.py`



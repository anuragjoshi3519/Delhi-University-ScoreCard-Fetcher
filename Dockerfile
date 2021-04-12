FROM ubuntu:20.04

MAINTAINER anurag_joshi@outlook.com

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y tzdata
RUN apt-get install -y wkhtmltopdf && apt-get --fix-broken install
RUN apt-get install -y tesseract-ocr 
RUN apt-get install -y libtesseract-dev
RUN apt-get install -y python3-pip 
RUN apt-get install -y python3-venv
RUN apt-get install -y git

RUN git clone --single-branch --branch dev2021 https://github.com/anuragjoshi3519/Delhi-University-ScoreCard-Fetcher.git

WORKDIR "Delhi-University-ScoreCard-Fetcher/"

RUN python3 -m venv env
RUN /bin/bash -c "source env/bin/activate"
RUN pip3 install -r requirements.txt
RUN mkdir Downloads/

CMD ["python3","fetchScoreCard.py"]

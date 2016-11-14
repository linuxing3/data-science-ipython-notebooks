FROM frolvlad/alpine-python2 
MAINTAINER Xing Wenju "linuxing3@qq.com"

RUN apk add --no-cache curl py-curl
RUN apk add --no-cache gcc 
RUN pip install pyspider 
RUN pip install scrapy 

CMD pyspider all

FROM linuxing3/keras:pyspider 
MAINTAINER Xing Wenju "linuxing3@qq.com"

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Setting a another volume mount point
VOLUME /notebooks
WORKDIR /notebooks

# Users to login
USER root

# Command Entry
CMD /home/condauser/anaconda3/bin/pyspider all

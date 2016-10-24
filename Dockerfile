FROM xblaster/tensorflow-jupyter
MAINTAINER Xing Wenju "linuxing3@qq.com"

# Original repository
# https://github.com/xblaster/dockerfiles/tree/master/tensorflow-jupyter

# Create conda user, get anaconda by web or locally
# RUN useradd --create-home --home-dir /home/condauser --shell /bin/bash condauser
# Set persistent environment variables for python3 and python2
ENV PY2PATH=/home/condauser/anaconda3/envs/python2/bin
ENV PY3PATH=/home/condauser/anaconda3/bin

# Run conda install from conda-forge repositories
RUN $PY3PATH/conda install -c conda-forge keras tensorflow theano

# Setting a another volume mount point
VOLUME /notebooks
WORKDIR /notebooks

# Users to login
USER root

# Command Entry
CMD $PY3PATH/jupyter notebook --no-browser --ip=0.0.0.0
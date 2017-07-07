FROM ubuntu:16.04

MAINTAINER Mikkel Vilstrup <mikkel@vilstrup.dk>

ARG KERAS_VERSION=2.0.5

##############################################################################
# Install TensorFlow dependencies
##############################################################################
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libfreetype6-dev \
        libpng12-dev \
        libzmq3-dev \
        pkg-config \
        python \
        python-dev \
        git \
        rsync \
        software-properties-common \
        unzip \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

##############################################################################
# Install Anaconda
##############################################################################
RUN apt-get update && \
    apt-get install -y wget bzip2 ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN wget --quiet https://repo.continuum.io/archive/Anaconda3-4.4.0-Linux-x86_64.sh && \
    /bin/bash Anaconda3-4.4.0-Linux-x86_64.sh -b -p /opt/conda && \
    rm Anaconda3-4.4.0-Linux-x86_64.sh

ENV PATH /opt/conda/bin:$PATH
RUN pip install --upgrade pip

##############################################################################
# Install TensorFlow
##############################################################################
RUN conda install -c conda-forge tensorflow=1.1.0


##############################################################################
# Install Keras
##############################################################################
RUN pip --no-cache-dir install git+git://github.com/fchollet/keras.git@${KERAS_VERSION}


##############################################################################
# Setup Jupyter
##############################################################################
COPY config.py /root/.jupyter/jupyter_notebook_config.py

# Copy sample notebooks.
COPY notebooks /notebooks

# Jupyter has issues with being run directly:
#   https://github.com/ipython/ipython/issues/7062
# We just add a little wrapper script.
COPY run_jupyter.sh /

# TensorBoard
EXPOSE 6006
# IPython
EXPOSE 8888

RUN export TF_CPP_MIN_LOG_LEVEL=2
# Tell docker where to go automatically
WORKDIR "/notebooks"

CMD ["/run_jupyter.sh", "--allow-root"]

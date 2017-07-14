# Build the standard serving environment
FROM dbrosius/tensorflow-serving-devel:latest


MAINTAINER Mikkel Vilstrup <mikkel@vilstrup.dk>

##############################################################################
# Set the appropriate configurations needed to build serving
##############################################################################
ARG CC_OPT_FLAGS="-march=native"
ARG NEED_JEMALLOC=1
ARG NEED_GCP=0
ARG NEED_HDFS=0
ARG ENABLE_XLA=0

# Which python path should be used?
ARG PYTHON_BIN_PATH="/usr/bin/python"
ARG PYTHON_LIB_PATH="/usr/local/lib/python2.7/dist-packages"

# Does your model use OPENCL ??
ARG NEED_OPENCL=0

# should it run on CUDA?? (No it is a CPU build)
ARG NEED_CUDA=0


RUN \
  update-ca-certificates -f && \
  git clone https://github.com/tensorflow/serving && \
  cd serving && \
  git submodule init && \
  git submodule update --recursive && \
  cd tensorflow && \
    PYTHON_BIN_PATH={PYTHON_BIN_PATH} \
    CC_OPT_FLAGS={CC_OPT_FLAGS} \
    TF_NEED_JEMALLOC={NEED_JEMALLOC} \
    TF_NEED_GCP={NEED_GCP} \
    TF_NEED_HDFS={NEED_HDFS} \
    TF_ENABLE_XLA={ENABLE_XLA} \
    PYTHON_LIB_PATH={PYTHON_LIB_PATH} \
    TF_NEED_OPENCL={NEED_OPENCL} \
    TF_NEED_CUDA={NEED_CUDA} ./configure && \
  cd .. && \
  bazel build -c opt tensorflow_serving/...

ENTRYPOINT ["/serving/bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server"]
CMD ["--port=9000","--model_name=inception","--model_base_path=/opt/tf-export","--use_saved_model=false"]

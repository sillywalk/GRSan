FROM ubuntu:16.04

WORKDIR /workspace
RUN apt update && apt install -y \
  build-essential \
  wget \
  vim \
  cmake \
  git \
  ninja-build \
  python3-dev \
  python-dev \
  bison 
COPY . /workspace

RUN cd llvm-7.0.0.build && sh baseline_dfsan_setup.sh
RUN cd llvm-7.0.0.build && sh configure.sh
RUN cd llvm-7.0.0.build && sh make.sh

CMD [ "/bin/bash" ]

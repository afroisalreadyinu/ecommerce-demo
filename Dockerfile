FROM ubuntu:16.04

RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install --upgrade pip

ADD . /ecommerce-demo
WORKDIR /ecommerce-demo

RUN pip3 install -e .

CMD run-ecomm-demo

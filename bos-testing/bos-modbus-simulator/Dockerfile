
FROM  balenalib/raspberry-pi-debian-python:bullseye

RUN sudo apt-get update
RUN sudo apt-get -y install python-dev python-setuptools build-essential python3-pip
RUN sudo apt-get -y install wget
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

RUN sudo mkdir /opt/bos-modbus-simulator
COPY * /opt/bos-modbus-simulator

WORKDIR /opt/bos-modbus-simulator
RUN python3 -m pip install wheel
RUN python3 -m pip install -r requirements.txt

EXPOSE 502

CMD sudo python3 bos-modbus-server.py

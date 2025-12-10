#!/usr/bin/env bash
#apt install software-properties-common -y
#add-apt-repository ppa:deadsnakes/ppa
#apt update -y
#apt-get install -y python3.12
#python3.12 --version
#curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12
#pip3.12 -V
apt-get install -y python3 python3-pip python3-dev python3-tk xvfb
pip3 install -r /autograder/source/requirements.txt

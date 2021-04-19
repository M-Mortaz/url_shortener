FROM ubuntu:18.04
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y python3.7 python3.7-dev python3-pip zip

#Add requirements.txt to docker image
ADD ./requirements.txt /

#Install python packages
RUN python3.7 -m pip install -r requirements.txt

#Make logs directory
RUN mkdir -p /logs/uwsgi/
RUN mkdir -p /logs/django/

#Copy source codes and make shared directory
RUN mkdir -p /socket

ADD ./ /docker_api/



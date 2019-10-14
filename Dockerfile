# Used by docker-build as a base image for the api
FROM centos/python-35-centos7
COPY requirements.txt .
RUN /bin/bash -c 'pip install -r requirements.txt'

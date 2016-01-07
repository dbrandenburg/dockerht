FROM centos:7
RUN yum -y install nc
CMD while true; do echo hello |nc -l 80;done

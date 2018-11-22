#use latest armv7hf compatible debian version from group resin.io as base image
FROM resin/armv7hf-debian:stretch

#enable building ARM container on x86 machinery on the web (comment out next line if not built as automated build on docker hub) 
RUN [ "cross-build-start" ]

#labeling
LABEL maintainer="ga83mir@mytum.de" \
      version="V0.9.1.0" \
      description="netpu"

#copy files
COPY "./init.d/*" /etc/init.d/ 
COPY "./driver/*" "./firmware/*" /tmp/

#do installation
RUN apt-get update  \
    && apt-get install -y openssh-server build-essential \
    && apt-get install -y openssh-server net-tools \
    && apt-get install -y --no-install-recommends apt-utils \
    && apt-get install python \
    && apt-get install python-pip \
    && apt-get install nano \
    && apt-get install python-dev \
    && apt-get install libxml2-dev libxmlsec1-dev libffi-dev gcc \

#do users root and pi    
    && useradd --create-home --shell /bin/bash pi \
    && echo 'root:root' | chpasswd \
    && echo 'pi:PWD4ais!' | chpasswd \
    && adduser pi sudo \
    && mkdir /var/run/sshd \
    && sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd \

    && touch /usr/bin/modprobe \
    && chmod +x /usr/bin/modprobe \
    && touch /etc/modules \
#install netX driver and netX ethernet supporting firmware
    && dpkg -i /tmp/netx-docker-pi-drv-1.1.3.deb \
    && dpkg -i /tmp/netx-docker-pi-pns-eth-3.12.0.8.deb \
#compile netX network daemon
    && gcc /tmp/cifx0daemon.c -o /opt/cifx/cifx0daemon -I/usr/include/cifx -Iincludes/ -lcifx -pthread \

#install docker	
    && curl -sSL https://get.docker.com | sh \
#clean up
    && rm -rf /tmp/* \
    && apt-get remove build-essential \
    && apt-get -yqq autoremove \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*

#create needed folders for python program
RUN mkdir /home/pi/opc_http
RUN mkdir /home/pi/opc_http/log_file /home/pi/opc_http/module /home/pi/opc_http/test \
	  /home/pi/ua_python3 /home/pi/ua_python3/log_file /home/pi/ua_python3/module \
	  /home/pi/ua_python3/test

#do install pip
RUN sudo pip install --upgrade setuptools
RUN sudo apt-get update && sudo apt-get upgrade
RUN pip install wheel
RUN pip install requests
RUN pip install opcua

#set the workding directory for programming examples
WORKDIR /home/pi

#copy opc http files
COPY ./opc_http/log_file/* opc_http/log_file/
COPY ./opc_http/module/* opc_http/module/
COPY ./opc_http/test/* opc_http/test/
COPY ./opc_http/opc_ua_client_http.py opc_http/opc_ua_client_http.py

#copy ua python3 files
COPY ./ua_python3/log_file/* ua_python3/log_file/
COPY ./ua_python3/module/* ua_python3/module/
COPY ./ua_python3/test/* ua_python3/test/
COPY ./ua_python3/opcua3.py ua_python3/opcua3.py

#set the entrypoint
ENTRYPOINT ["/etc/init.d/entrypoint.sh"]

#do ports
EXPOSE 22 1217 4840

#set STOPSGINAL
STOPSIGNAL SIGTERM

#stop processing ARM emulation (comment out next line if not built as automated build on docker hub @haha)
RUN [ "cross-build-end" ]


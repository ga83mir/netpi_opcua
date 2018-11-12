#use latest armv7hf compatible debian version from group resin.io as base image
FROM resin/armv7hf-debian:stretch

#enable building ARM container on x86 machinery on the web (comment out next line if not built as automated build on docker hub) 
RUN [ "cross-build-start" ]

#labeling
LABEL maintainer="netpi@hilscher.com" \
      version="V0.9.1.0" \
      description="netX based TCP/IP network interface and codesys"

#version
ENV HILSCHERNETPI_NETX_TCPIP_NETWORK_INTERFACE_VERSION 0.9.1.0

#copy files
COPY "./init.d/*" /etc/init.d/ 
COPY "./driver/*" "./firmware/*" /tmp/

#do installation
RUN apt-get update  \
    && apt-get install -y openssh-server build-essential \
    && apt-get install -y openssh-server net-tools \
#do users root and pi    
    && useradd --create-home --shell /bin/bash pi \
    && echo 'root:root' | chpasswd \
    && echo 'pi:raspberry' | chpasswd \
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
#RUN mkdir /home/pi/rasp /home/pi/opc_http /home/pi/ua_python3 \

#set the workding directory for programming examples
WORKDIR /home/pi
RUN ls
RUN mkdir rasp opc_http ua_python3


#copy Rasp Files
COPY ./rasp/* rasp/

#copy opc http files
COPY ./opc_http/* opc_http/

#copy ua python3 files
COPY ./ua_python3/* ua_python3/

#set the entrypoint
ENTRYPOINT ["/etc/init.d/entrypoint.sh"]

#do ports
EXPOSE 22 1217 4840

#set STOPSGINAL
STOPSIGNAL SIGTERM

#stop processing ARM emulation (comment out next line if not built as automated build on docker hub @haha)
RUN [ "cross-build-end" ]










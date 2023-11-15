# Use the official Debian Buster as a base image
FROM debian:buster

# Update packages and install necessary software
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    curl \
    procps \
    libncurses5 \
    libncurses5-dev

# Install FirebirdSS-2.5.9
RUN curl -Lo /tmp/fb259.tar.gz \
    https://github.com/FirebirdSQL/firebird/releases/download/R2_5_9/FirebirdSS-2.5.9.27139-0.amd64.tar.gz
RUN mkdir -p /tmp/firebird
RUN tar -xzf /tmp/fb259.tar.gz -C /tmp/firebird --strip-components=1
RUN rm /tmp/fb259.tar.gz
RUN chmod +x /tmp/firebird/install.sh
RUN ( cd /tmp/firebird ; ./install.sh -silent )
RUN rm -r /tmp/firebird
RUN ln -s /opt/firebird/bin/gbak /usr/bin/gbak
RUN ln -s /opt/firebird/bin/gdef /usr/bin/gdef
RUN ln -s /opt/firebird/bin/gfix /usr/bin/gfix
RUN ln -s /opt/firebird/bin/gpre /usr/bin/gpre
RUN ln -s /opt/firebird/bin/gsec /usr/bin/gsec
RUN ln -s /opt/firebird/bin/gsplit /usr/bin/gsplit
RUN ln -s /opt/firebird/bin/gstat /usr/bin/gstat
RUN ln -s /opt/firebird/bin/isql /usr/bin/isql
RUN ln -s /opt/firebird/bin/nbackup /usr/bin/nbackup

RUN curl -Lo /tmp/fbexport.tar.gz https://www.firebirdfaq.org/files/fbexport-1.90.tar.gz
RUN mkdir -p /tmp/fbexport
RUN tar -xzf /tmp/fbexport.tar.gz -C /tmp/fbexport --strip-components=1
RUN ln -s /opt/firebird/lib/libfbclient.so.2.5.9 /lib/x86_64-linux-gnu/libfbclient.so.2
RUN ( cd /tmp/fbexport ; make )
RUN mv /tmp/fbexport/exe/fbexport /usr/bin
RUN mv /tmp/fbexport/exe/fbcopy /usr/bin
RUN rm -r /tmp/fbexport

# Set the working directory inside the container
WORKDIR /app

# Copy your application files into the container (if applicable)
# COPY ./app /app

# Define any environment variables if needed
# ENV MY_VAR=value

# Expose any necessary ports (if your application requires it)
# EXPOSE 8080

# Define the command to run your application
CMD ["/usr/bin/python3", "fbtocsv.py"]
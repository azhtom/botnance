FROM python:3.7.9

MAINTAINER Daniel Soria <@azhtom>

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y python3-dev

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install

RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz

COPY src/requirements.txt ./

RUN pip install -r requirements.txt

COPY src .

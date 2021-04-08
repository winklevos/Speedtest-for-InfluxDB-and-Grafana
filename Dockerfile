FROM python:alpine
LABEL maintainer="winklevos@outlook.com"

VOLUME /src/
COPY influxspeedtest.py requirements.txt /src/
COPY config.ini-dist /src/config.ini
ADD influxspeedtest /src/influxspeedtest
WORKDIR /src

RUN pip install -r requirements.txt

CMD ["python", "-u", "/src/influxspeedtest.py"]

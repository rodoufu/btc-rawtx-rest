FROM python:3.7.6-slim
MAINTAINER Rodolfo Araujo <rodoufu@gmail.com>

RUN mkdir app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt \
    && pip3 install connexion[swagger-ui]

COPY *.py /app/
COPY swagger.yml /app

WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["server.py"]

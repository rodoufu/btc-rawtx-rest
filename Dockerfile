FROM python:3.7.6-alpine
MAINTAINER Rodolfo Araujo <rodoufu@gmail.com>

RUN mkdir app
COPY requirements.txt *.py swagger.yml /app/
RUN pip3 install -r /app/requirements.txt \
    && pip3 install connexion[swagger-ui]

WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["server.py"]

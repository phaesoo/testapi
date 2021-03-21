#
# TestAPI
#
# build:
#   docker build --force-rm -t phaesoo/testapi .
# run:
#   docker run --rm -it --name testapi -p 80:8080 phaesoo/testapi

FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./app /app

COPY ./requirements.txt ./uwsgi.ini /app/

RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt

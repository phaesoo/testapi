FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./app /app

COPY ./requirements.txt ./uwsgi.ini /app/

RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt

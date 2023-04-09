FROM python:3.10.6

WORKDIR /application

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src .

EXPOSE 8000

VOLUME /data

CMD [ "python", "./init.py" ]

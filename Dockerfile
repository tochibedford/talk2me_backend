FROM python:3.10.6

WORKDIR /application

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src .

RUN mkdir /application/data && chown -R 1000:1000 /application/data

EXPOSE 8000

CMD [ "python", "./init.py" ]

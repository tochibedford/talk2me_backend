FROM python:3.10.6

WORKDIR /application

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src .

CMD [ "python", "./init.py" ]

EXPOSE 8000

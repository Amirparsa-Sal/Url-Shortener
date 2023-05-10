FROM python:3.9.16-alpine3.17

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./* /code/

RUN source .env

CMD ["python3", "main.py"]
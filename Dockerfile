FROM python:3.10.15-alpine3.19

WORKDIR /api-test

COPY . /api-test/

RUN pip install -r requirement.txt

EXPOSE 5000
CMD python3 app.py

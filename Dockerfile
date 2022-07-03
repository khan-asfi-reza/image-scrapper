FROM python:3.10-slim

WORKDIR /scrapperAPI

COPY requirements.txt requirements.txt

RUN apt-get update -y

RUN apt-get install -y libcairo2-dev

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
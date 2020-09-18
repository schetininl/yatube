FROM python:3.8.2

WORKDIR /app

COPY requirements.txt ./

RUN pip install --disable-pip-version-check -r requirements.txt

COPY yatube/ ./

EXPOSE 80
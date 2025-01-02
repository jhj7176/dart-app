FROM python:3.11
# FROM --platform=linux/amd64 python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app


COPY requirements.txt requirements.txt
# install python dependencies
RUN pip install -U setuptools pip
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# RUN python manage.py migrate

EXPOSE 8000
EXPOSE 8091

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]

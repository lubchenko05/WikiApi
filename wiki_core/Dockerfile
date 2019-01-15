# Pull base image
FROM python:3.6-alpine

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



# Copy requirements inside docker

COPY ./requirements.txt /wiki_core/requirements.txt

# Set work directory
WORKDIR /wiki_core

# Setup driver for psql
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev

# Install requirements
RUN pip install -r requirements.txt

# Copy project
COPY . /wiki_core/


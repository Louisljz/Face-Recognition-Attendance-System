FROM python:3.10.4
LABEL maintainer="Louis Jefferson Zhang <louis.ljz08@gmail.com>"

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Build Dependencies for Opencv, Dlib and Psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopencv-dev \
    libdlib-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# MAIN
WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./fr_as .

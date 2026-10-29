# Dockerfile for django-news-app
#
# Builds an image that runs the Django News site with Django's
# development server. The image holds no settings or secrets: they are
# passed in from a .env file when a container starts, for example:
#     docker build -t django-news-app .
#     docker run --env-file .env -p 8000:8000 django-news-app

# Start from the official Python 3.13 image, the version the project is
# built with. "slim" is a smaller version: a minimal Debian Linux with
# Python installed, but without the compilers and extra tools of the
# full image.
FROM python:3.13-slim

# PYTHONDONTWRITEBYTECODE: do not write .pyc files into the image.
# PYTHONUNBUFFERED: print the server's output straight away, so it
# shows up in docker logs as it happens.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create the /app folder inside the image and work from there.
WORKDIR /app

# mysqlclient, the package Django uses to talk to MariaDB, is compiled
# when it is installed on Linux, so it needs a C compiler (gcc),
# pkg-config, and the MariaDB client library's development files. The
# slim image has none of these. Removing apt's package lists afterward
# keeps them out of the image.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        pkg-config \
        default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file, then install what it lists. Docker
# saves the result of each step and skips that step on the next build
# if its files have not changed. Because the code is copied in a later
# step, editing the code does not cause the packages to be installed
# again; that only happens when requirements.txt changes.
# --no-cache-dir keeps pip's download cache out of the image, making it
# smaller.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project into /app in the image. .dockerignore keeps .env,
# venv, and other files that do not belong in an image out of it.
COPY . .

# The port the development server listens on, for documentation and
# tools. docker run -p 8000:8000 is what makes it reachable.
EXPOSE 8000

# Start the development server when a container runs. 0.0.0.0 makes it
# listen on every network address inside the container, so requests
# from outside the container reach it. The default, 127.0.0.1, would
# only answer requests from inside the container itself.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

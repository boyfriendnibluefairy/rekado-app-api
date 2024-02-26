# we use alphine as base image because it is lightweight.
# FROM ubuntu:latest
# from https://hub.docker.com/_/python, 3.9-alphine3.13 does not exist anymore
#FROM python:3.9.18-alphine
FROM python:3.13.0a4-slim-bullseye

# name of the developer who will maintain this
LABEL maintainer="boyfriendnibluefairy"

# tells Docker that you don't want to store the output,
# in other words, just directly show the output in the screen
ENV PYTHONUNBUFFERED 1

# copy resources from local computer to the container
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

# when we run commands on our Docker image, it will look for a default directory
# to execute those commands. WORKDIR defines this default directory
WORKDIR /app

# EXPOSE keyword tells Docker that a container listens for traffic on the
# specified port. When the container is running a web server, this informs
# Docker that the web server will listen on port XXXX for TCP connections.
# TCP is the default protocol.
EXPOSE 8000

# Shell command that tells us to execute the next command only if
# the preceding command is successful.
# &&

# "\" backslash means override any existing aliases.
# Alias is a shortcut name for a command.

# Create python virtual environment.
# python -m venv /py

# Upgrade "pip" inside our python virtual environment.
# /py/bin/pip install --upgrade pip

# Install requirements.txt in our python virtual environment.
# /py/bin/pip install -r /tmp/requirements.txt 

# Remove other files and dependencies not useful to our project to keep the
# environment as lightweight as possible.
# rm -f /tmp

# If we don't include the command "adduser", then the default user is root.
# For security purposes, we do not recommend running the env in root user mode.
# We just gave a name "django-user" to this non-root user.
# adduser django-user

# To keep Docker images as lightweight as possible, we do not require a password from
# the user and no need to create a separate folder for the user
# --disabled-password --no-create-home

# DEV=false argument was added because we would like to
# separate DEBUG mode dependencies of our project
# with the RELEASE mode dependencies of our project.
ARG DEV=false

# RUN python -m venv /py && \
#     /py/bin/pip install --upgrade pip && \
#     /py/bin/pip install -r /tmp/requirements.txt && \
#     rm -f /tmp && \
#     adduser \
#         --disabled-password \
#         --no-create-home \
#         django-user

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Update the environment variable
ENV PATH="/py/bin:$PATH"

# Before the line "USER django-user", all commands are run as root user.
# After the line "USER django-user", commands are now run as django-user user.
# This means USER command is like user switch or user login, eventually updating /etc/passwd
USER django-user
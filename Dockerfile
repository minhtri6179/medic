# pull official base image
FROM --platform=linux/amd64 python:3.10

# set work directory
WORKDIR /usr/src/app


# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt


# copy project
COPY . .



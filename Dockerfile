# base image  
FROM --platform=linux/amd64 python:3.10   

WORKDIR /code
# set environment variables  

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip  
# run this command to install all dependencies  
RUN pip install -r requirements.txt  

# copy whole project to your docker home directory. 
COPY . .  

# start server  
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]  
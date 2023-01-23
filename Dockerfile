# install latest python
FROM python:latest

# set working directory
WORKDIR /usr/src/app

# set environment variables
# timezone to +7
ENV TZ=Asia/Jakarta

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

# command to run on container start
CMD [ "python", "./main.py" ]

# export port 5000
EXPOSE 5000
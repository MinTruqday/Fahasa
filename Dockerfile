# For more information, please refer to https://aka.ms/vscode-docker-python
#FROM python:3-slim
FROM python:3

# Keeps Python from generating .pyc files in the container
#ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
#ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Install pip requirements
COPY requirements.txt ./
#RUN python -m pip install -r requirements.txt
RUN pip install --trusted-host pypi.install.org -r requirements.txt

RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

#WORKDIR /app
#COPY . /app
COPY . .

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
#RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
#USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "PiBook.py"]
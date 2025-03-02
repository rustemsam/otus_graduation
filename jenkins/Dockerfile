FROM jenkins/jenkins

USER root

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget unzip \
    libglib2.0-0 \
    chromium \
    firefox-esr \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    netcat-openbsd  \
    && apt-get clean


COPY requirements.txt /tmp/requirements.txt

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --break-system-packages -r /tmp/requirements.txt

USER jenkins
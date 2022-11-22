FROM fedora:latest
RUN dnf install python3-prometheus_client.noarch -y
WORKDIR /usr/app/src
COPY run.py ./
CMD [ "python3", "./run.py"]

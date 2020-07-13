FROM python:3.6.9

COPY auth/requirements.txt /
RUN pip3 install -r /requirements.txt

RUN mkdir -p /build
WORKDIR /build

COPY auth /build
COPY common /build/common

EXPOSE 5000

ENV C_FORCE_ROOT="true"

# NOTE: this line for debuging
# CMD ["bash", "-c", "while true; do echo; sleep 2; done"]

CMD ["honcho", "start"]
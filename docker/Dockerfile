FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
	dpkg-dev \
	gcc \
	libbluetooth-dev \
	libbz2-dev \
	libc6-dev \
	libexpat1-dev \
	libffi-dev \
	libgdbm-dev \
	liblzma-dev \
	libncursesw5-dev \
	libreadline-dev \
	libsqlite3-dev \
	libssl-dev \
	make \
	tk-dev \
	uuid-dev \
	wget \
	xz-utils \
	zlib1g-dev

# ------ Setup Python Environment ------
COPY requirements.txt /opt/
WORKDIR /opt
RUN pip3 install -r requirements.txt

RUN apt-get install -y --no-install-recommends vim ffmpeg

RUN mkdir /root/panns_data
COPY data/Cnn14_DecisionLevelMax.pth /root/panns_data/
COPY data/class_labels_indices.csv /root/panns_data/

RUN mkdir /root/deepspeech_data
COPY data/deepspeech-0.9.3-models-zh-CN.pbmm /root/deepspeech_data/
COPY data/deepspeech-0.9.3-models-zh-CN.scorer /root/deepspeech_data/
COPY data/deepspeech-0.9.3-models.pbmm /root/deepspeech_data/
COPY data/deepspeech-0.9.3-models.scorer /root/deepspeech_data/

COPY src /opt/src
RUN mkdir /opt/src/data

COPY tests /opt/tests

WORKDIR /opt/src

EXPOSE 5000
# CMD ["python3", "app.py"]
CMD ["python3", "while.py"]


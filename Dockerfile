FROM python:3.7.6

RUN apt-get update && apt-get install -y libgl1-mesa-glx

RUN git clone https://github.com/puleon/SimpleHTR.git

WORKDIR /SimpleHTR

RUN pip install -r requirements.txt

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /SimpleHTR

RUN rm -r model

RUN wget http://files.deeppavlov.ai/htr_fb/model.tar.gz

RUN tar -xvzf model.tar.gz

RUN cp model/corpus.txt data

RUN cp model/corpus.txt data

WORKDIR /SimpleHTR/src

COPY *.py ./

ARG SERVICE_PORT
ENV SERVICE_PORT ${SERVICE_PORT}

HEALTHCHECK --interval=5s --timeout=90s --retries=3 CMD curl --fail 127.0.0.1:${SERVICE_PORT}/healthcheck || exit 1

CMD gunicorn --workers=1 server:app -b 0.0.0.0:${SERVICE_PORT} --timeout=300

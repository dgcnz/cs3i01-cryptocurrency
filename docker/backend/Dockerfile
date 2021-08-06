FROM python:3.9.6

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY lib lib
COPY minernode.py minernode.py
COPY walletnode.py walletnode.py
COPY .tfc .tfc
COPY config.yaml config.yaml

EXPOSE $PORT

CMD python ${FLASK_APP}

FROM python:3.9-slim
RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt
ENV PYTHONUNBUFFERED 1
COPY s3do/ /src/s3do/
COPY s3do.py /src
ENTRYPOINT ["./s3do.py"]

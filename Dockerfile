FROM python:3.12-slim

ENV PUID=1000
ENV PGID=1000

RUN mkdir /arlo-downloader /records /arlo-downloader/aarlo && \
    groupadd -g ${PGID} arlo-downloader && \
    useradd -u ${PUID} -g arlo-downloader arlo-downloader && \
    chown -R arlo-downloader:arlo-downloader /records /arlo-downloader

WORKDIR /arlo-downloader

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY arlo-downloader.py config.py entrypoint.sh ./
RUN chmod +x entrypoint.sh

USER arlo-downloader

ENTRYPOINT ["/arlo-downloader/entrypoint.sh"]

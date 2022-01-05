FROM python:3.7-slim

RUN pip install --upgrade pip

RUN adduser arlo-downloader
RUN mkdir -p /media
RUN chown arlo-downloader:arlo-downloader /media

USER arlo-downloader

WORKDIR /

COPY --chown=arlo-downloader:arlo-downloader requirements.txt requirements.txt
COPY --chown=arlo-downloader:arlo-downloader arlo-downloader.py /arlo-downloader.py

RUN pip install --user -r requirements.txt

CMD [ "python", "/arlo-downloader.py", "--save-media", "/media/${Y}/${m}/${F}T${t}_${N}_${SN}"]

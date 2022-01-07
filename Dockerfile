FROM python:3.7-slim

RUN pip install --upgrade pip

RUN adduser arlo-downloader
RUN mkdir -p /media
RUN chown arlo-downloader:arlo-downloader /media

USER arlo-downloader

WORKDIR /

COPY --chown=arlo-downloader:arlo-downloader requirements.txt requirements.txt
COPY --chown=arlo-downloader:arlo-downloader arlo-downloader.py /arlo-downloader.py
COPY --chown=arlo-downloader:arlo-downloader config.py /config.py
COPY --chown=arlo-downloader:arlo-downloader entrypoint.sh /entrypoint.sh

RUN pip install --user -r requirements.txt

ENV TFA_TYPE=PUSH
ENV TFA_SOURCE=push
ENV TFA_RETRIES=10
ENV TFA_DELAY=5
ENV TFA_HOST=_invalid
ENV TFA_USERNAME=_invalid
ENV TFA_PASSWORD=_invalid

ENTRYPOINT ["/entrypoint.sh"]

CMD [                                                                       \
    "python",               "/arlo-downloader.py",                          \
        "--save-media-to",  "'/media/${Y}/${m}/${F}T${t}_${N}_${SN}.mp4'",  \
        "--tfa-type",       "${TFA_TYPE}",                                  \
        "--tfa-source",     "${TFA_SOURCE}",                                \
        "--tfa-retries",    "${TFA_RETRIES}",                               \
        "--tfa-delay",      "${TFA_DELAY}",                                 \
        "--tfa-host",       "${TFA_HOST}",                                  \
        "--tfa-username",   "{$TFA_USERNAME}",                              \
        "--tfa-password",   "{$TFA_PASSWORD}"                               \
    ]

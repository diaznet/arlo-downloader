FROM python:3.7-slim

# Create the working directories
RUN mkdir /arlo-downloader /records

# Add user
RUN useradd arlo-downloader

# Switch to arlo-downloader directory
WORKDIR /arlo-downloader

COPY requirements.txt arlo-downloader.py config.py entrypoint.sh .

# Update PIP to latest version and install required package(s)
RUN pip install --upgrade pip && pip install -r requirements.txt

# Setting our entrypoint
ENTRYPOINT ["/arlo-downloader/entrypoint.sh"]

# Start the arlo-downloader.py script
CMD [                                                                       \
    "python",               "/arlo-downloader/arlo-downloader.py",          \
        "--save-media-to",  "'/records/${Y}/${m}/${F}T${t}_${N}_${SN}'",    \
        "--tfa-type",       "${TFA_TYPE:=PUSH}",                                  \
        "--tfa-source",     "${TFA_SOURCE:=push}",                                \
        "--tfa-retries",    "${TFA_RETRIES:=10}",                               \
        "--tfa-delay",      "${TFA_DELAY:=5}",                                 \
        "--tfa-host",       "${TFA_HOST:=:=_invalid}",                                  \
        "--tfa-username",   "{$TFA_USERNAME:=_invalid}",                              \
        "--tfa-password",   "{$TFA_PASSWORD:=_invalid}"                               \
    ]

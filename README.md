# Arlo-Downloader

[![](https://img.shields.io/docker/image-size/diaznet/arlo-downloader/latest)](https://hub.docker.com/r/diaznet/arlo-downloader)
[![](https://img.shields.io/docker/pulls/diaznet/arlo-downloader?color=%23099cec)](https://hub.docker.com/r/diaznet/arlo-downloader)

Automatically download your videos from Arlo for long-term storage.

# Introduction

In the free tier of Arlo, customers are entitled to keep up to 7 days of recording in Arlo "cloud" storage. After 7 days, the recordings are deleted.
In order to ensure the camera recordings are permanently backup'ed, we'll automate the downloading of the videos.

# Features

- Downloads all recordings available from Arlo cloud storage locally.
- Handles TFA with EMAIL or PUSH methods (see below and [instructions](https://github.com/twrecked/pyaarlo#2fa-imap) for EMAIL type)


# Requirements

- Arlo cameras and My Arlo account, obviously.
- Docker _(if you are new to Docker, see [Installing Docker and Docker Compose](https://dev.to/rohansawant/installing-docker-and-docker-compose-on-the-raspberry-pi-in-5-simple-steps-3mgl))_
- Arlo Mobile App, if using TFA with PUSH method.

# Instructions

## Create a dedicated user for Arlo API Access

Although not mandatory, it is STRONGLY recommended to create a dedicated, less-privileged user in My Arlo that will connect to the API.  
This way your main account is not used by Arlo Downloader and access can be revoked if needed.

- Connect to [my.arlo.com](https://my.arlo.com) with your regular username and password.
- Go to **Settings**, then **Grant Access** section.
- Add a friend with button **Add** then fill in required information. This will effectively create a new user attached to your main account.
- Select the cameras you wish to have access to.
  - Important: Downloading recordings does not require **Allow Access Rights** to be ticked. Leaving it unticked creates a read-only account.
- Click **Send Invite** and follow instructions sent by email to set-up new account and password.
  - Note: if you use the default Push auth method for TFA, log-in once with the new account in the mobile Arlo App and trust the device, so you can receive push notifications on this device.

## Create the container

### Parameters

#### Mandatory

| Parameter | Function |
| :----: | --- |
| -e `ARLO_USERNAME` | The username required to access Arlo API |
| -e `ARLO_PASSWORD` | The password for the username above |
| -v `/records` | Storage for downloaded records |

#### Optional

| Parameter | Function | Default |
| :----: | --- | --- |
| -e `TFA_TYPE` | Arlo TFA type. Currently only supports push,email | push |
| -e `TFA_SOURCE` | Arlo TFA type. Currently only supports push,imap | push |
| -e `TFA_RETRIES` | Arlo TFA retries. | 10 |
| -e `TFA_DELAY` | Arlo TFA Delay between each check | 5 |
| -e `TFA_HOST` | TFA_TYPE=EMAIL + TFA_SOURCE=imap only [Instructions](https://github.com/twrecked/pyaarlo#2fa-imap) | |
| -e `TFA_USERNAME` | TFA_TYPE=EMAIL + TFA_SOURCE=imap only [Instructions](https://github.com/twrecked/pyaarlo#2fa-imap) | |
| -e `TFA_PASSWORD` | TFA_TYPE=EMAIL + TFA_SOURCE=imap only [Instructions](https://github.com/twrecked/pyaarlo#2fa-imap) | |
| -e `DEBUG` | Set to 1 to enable debug logs | 0 |

#### Environment variables from files (Docker secrets)
You can set any environment variable from a file by using a special prepend FILE__.

As an example, instead of using -e ARLO_PASSWORD, you can set the following environment variable:

```bash
-e FILE__ARLO_PASSWORD=/run/secrets/myarlopassword
```

It will then set the environment variable ARLO_PASSWORD based on the contents of the /run/secrets/myarlopassword file.


### docker-compose

Create a file called docker-compose.yml with the following content: 

```yaml
version: "2.1"
services:
  arlo-downloader:
    image: diaznet/arlo-downloader:latest
    build: .
    container_name: arlo-downloader:latest
    environment:
      - ARLO_USERNAME=<api_username>
      - ARLO_PASSWORD=<password>
    volumes:
      - /path/to/videos:/records
    restart: unless-stopped
```

Note: you are also going to need the various TFA_* environmetn variables if yu have 2FA activated on your account.

Build and start the docker containers with docker-compose up. To run the containers in the background add the -d flag:

```bash
docker-compose up --build -d
```

### docker cli

```bash
docker run -d \
  --name=arlo-downloader \
  -e ARLO_USERNAME=<api_username> \
  -e ARLO_PASSWORD=<password> \
  -v /path/to/videos:/records \
  --restart unless-stopped \
  diaznet/arlo-downloader:latest
```

Once the container is started, it will first download into /path/to/videos all available recordings from the API.  
If files already exist, they will not be replaced.  
It will then run indefinitely and download any new recording as soon as it becomes available in the API.

Default Naming scheme:

    <year>/<month_number>/<year>-<month_number>-<day_number>T<hour>:<minute>:<seconds>_<device_name>_<device_serial_number>

## Manual Script run

The script can also be ran manually.

```bash
usage: arlo-downloader.py [-h] [-d] [-m SAVE_MEDIA_TO] [-t {PUSH,EMAIL}] [-s {push,imap}] [-r TFA_RETRIES]
                          [-T TFA_DELAY] [-H TFA_HOST] [-U TFA_USERNAME] [-P TFA_PASSWORD]

Download records from Arlo Cameras.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Enable Debug messages. Can also be set with environment variable DEBUG=1
  -m SAVE_MEDIA_TO, --save-media-to SAVE_MEDIA_TO
                        Save Media naming scheme without extension (default = '/records/
                        ${Y}/${m}/${F}T${t}_${N}_${SN}')
  -t {PUSH,EMAIL}, --tfa-type {PUSH,EMAIL}
                        Set TFA type (default = 'PUSH')
  -s {push,imap}, --tfa-source {push,imap}
                        Set TFA source (default = 'push')
  -r TFA_RETRIES, --tfa-retries TFA_RETRIES
                        Set TFA max retries (default = 10).
  -T TFA_DELAY, --tfa-timeout TFA_TIMEOUT
                        Set TFA timeout (default = 5).
  -H TFA_HOST, --tfa-host TFA_HOST
                        (EMAIL/imap only) Set TFA host (default = ).
  -U TFA_USERNAME, --tfa-username TFA_USERNAME
                        (EMAIL/imap only) Set TFA username (default = ).
  -P TFA_PASSWORD, --tfa-password TFA_PASSWORD
                        (EMAIL/imap only) Set TFA password (default = ).
```

# Disclaimer

This application comes without warranty.
Please use with care.
Any damage cannot be related back to the author.

# Todo's
- Ability to customize video filenames / filepath

# Credits
Author: Jeremy Diaz  
This container uses [pyaarlo](https://github.com/twrecked/pyaarlo) 0.8 library.

# Arlo-Downloader

[![](https://img.shields.io/docker/image-size/diaznet/arlo-downloader/latest)](https://hub.docker.com/r/diaznet/arlo-downloader)
[![](https://img.shields.io/docker/pulls/diaznet/arlo-downloader?color=%23099cec)](https://hub.docker.com/r/diaznet/arlo-downloader)

Automatically download your videos from Arlo for long-term storage.

# Introduction

In the free tier of Arlo, customers are entitled to keep up to 7 days of recording in Arlo "cloud" storage. After 7 days, the recordings are deleted.
In order to ensure the camera recordings are permanently backup'ed, it is necessary to automate the downloading of the videos.

# Features

Downloads all recordings available from Arlo cloud storage locally.
Naming scheme:

    <year>/<month_number>/<year>-<month_number>-<day_number>T<hour>:<minute>:<seconds>_<device_name>_<device_serial_number>.mp4

# Requirements

- Arlo cameras and My Arlo account, obviously.
- Docker _(if you are new to Docker, see [Installing Docker and Docker Compose](https://dev.to/rohansawant/installing-docker-and-docker-compose-on-the-raspberry-pi-in-5-simple-steps-3mgl))_

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

## Create the container

### Parameters

| Parameter | Function |
| :----: | --- |
| `ARLO_USERNAME` | The username required to access Arlo API |
| `ARLO_PASSWORD` | The password for the username above |
| `/media` | Storage for downloaded records |

### docker-compose

Create a file called docker-compose.yml with the following content: 

```yaml
version: "2.1"
services:
  arlo-downloader:
    image: diaznet/arlo-downloader
    container_name: arlo-downloader
    environment:
      - ARLO_USERNAME=<api_username>
      - ARLO_PASSWORD=<password>
    volumes:
      - /path/to/videos:/media
    restart: unless-stopped
```

Start the docker containers with docker-compose up. To run the containers in the background add the -d flag:

```bash
docker-compose up -d
```

### docker cli

```bash
docker run -d \
  --name=arlo-downloader \
  -e ARLO_USERNAME=<api_username> \
  -e ARLO_PASSWORD=<password> \
  -v /path/to/videos:/media \
  --restart unless-stopped \
  diaznet/arlo-downloader
```

Once the container is started, it will first download into /path/to/videos all available recordings from the API.  
If files already exist, they will not be replaced.  
It will then run indefinitely and download any new recording as soon as it becomes available in the API.



# Disclaimer

This application comes without warranty.
Please use with care.
Any damage cannot be related back to the author.

# Todo's
- Ability to customize video filenames / filepath
- Ability to enable DEBUG with docker compose / run

# Credits
Author: Jeremy Diaz  
This container uses [pyaarlo](https://github.com/twrecked/pyaarlo) 0.7.1.2 library.

#!/bin/bash

set -e
chown -R arlo-downloader:arlo-downloader /records
/bin/bash -l -c "$*"
exec exec runuser -u appuser "$@"
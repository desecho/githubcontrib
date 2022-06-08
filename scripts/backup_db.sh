#!/bin/bash

set -eou pipefail

TODAY="$(date +"%d-%m-%Y")"
FILENAME="${PROJECT}-${TODAY}.sql.gz"
mysqldump -u root -h "${DB_HOST}" "${PROJECT}" -p"${DB_PASSWORD}" | gzip -9 > "${FILENAME}"

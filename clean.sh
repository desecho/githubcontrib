#!/bin/bash

# We want to remove imports before running isort.
autoflake --remove-all-unused-imports --in-place -r ghcontrib ghcontrib_project

yapf -ri ghcontrib/tests/*.py ghcontrib/views ghcontrib/*.py ghcontrib_project
# This command takes a long time.
# yapf -ri ghcontrib/tests/fixtures/*.py

# We want to run isort after yapf to make sure isort lint pass.
isort -rc ghcontrib ghcontrib_project
csscomb ghcontrib/style/*
./eslint.sh
find . -type f -name "*.js" -not -path "./node_modules/*" -not -path "./ghcontrib/static/*" -exec js-beautify -r {} \;
find . -type f -name "*.json" -not -path "./node_modules/*" -not -path "./ghcontrib/static/*" -exec js-beautify -r {} \;

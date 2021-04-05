#!/bin/bash

# We want to remove imports before running isort.
autoflake --remove-all-unused-imports --in-place -r githubcontrib githubcontrib_project

yapf -ri githubcontrib/tests/*.py githubcontrib/views githubcontrib/*.py githubcontrib_project
unify -ri githubcontrib githubcontrib_project
# This command takes a long time.
# yapf -ri githubcontrib/tests/fixtures/*.py

# We want to run isort after yapf to make sure isort lint pass.
isort -rc githubcontrib githubcontrib_project
csscomb githubcontrib/styles/*
./eslint.sh
find . -type f -name "*.js" -not -path "./node_modules/*" -not -path "./githubcontrib/static/*" -not -path "./env/*" -exec js-beautify -r {} \;
find . -type f -name "*.json" -not -path "./node_modules/*" -not -path "./githubcontrib/static/*" -not -path "./env/*" -exec js-beautify -r {} \;

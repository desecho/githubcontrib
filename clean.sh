#!/bin/bash

# We want to remove imports before running isort.
autoflake --remove-all-unused-imports --in-place -r ghcontrib ghcontrib_project
yapf -ri ghcontrib ghcontrib_project
# We want to run isort after yapf to make sure isort lint pass.
isort -rc ghcontrib ghcontrib_project
csscomb ghcontrib/static/style.css
./eslint.sh
find ghcontrib/static/js -type f -name "*.js" -exec js-beautify -r {} \;
find . -type f -name "*.json" -not -path "./node_modules/*" -not -path "./ghcontrib/static/vendor/*" -exec js-beautify -r {} \;

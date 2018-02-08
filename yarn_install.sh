#!/bin/bash

mv node_modules node_modules_backup
yarn install --modules-folder ghcontrib/static/vendor --production
mv node_modules_backup node_modules

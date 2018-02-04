#!/bin/bash

autoflake --remove-all-unused-imports --in-place -r ghcontrib ghcontrib_project
yapf -ri ghcontrib ghcontrib_project
isort -rc ghcontrib ghcontrib_project

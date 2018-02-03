#!/bin/bash

isort -rc ghcontrib ghcontrib_project
yapf -ri ghcontrib ghcontrib_project

#!/bin/bash

set -eu

echo $(kubectl get pods -lapp=githubcontrib | grep Running | awk '{print $1}')

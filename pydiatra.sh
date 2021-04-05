#!/bin/bash

result=$(find githubcontrib -name '*.py' -exec py3diatra {} \;)
echo $result
if [[ $result ]]; then
	exit 1
fi

result=$(find githubcontrib_project -name '*.py' -exec py3diatra {} \;)
echo $result
if [[ $result ]]; then
    exit 1
fi

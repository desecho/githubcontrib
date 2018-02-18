#!/bin/bash

result=$(find ghcontrib -name '*.py' -exec py3diatra {} \;)
echo $result
if [[ $result ]]; then
	exit 1
fi

result=$(find ghcontrib_project -name '*.py' -exec py3diatra {} \;)
echo $result
if [[ $result ]]; then
    exit 1
fi

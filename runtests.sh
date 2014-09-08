#!/bin/bash

set -e

for folder in $(ls -d grammar-v*); do
    if [ -e $folder/validate.py ]; then
        echo "##"
        echo "## Validating test file in $folder"
        echo "##"
        python $folder/validate.py $folder/test.json
        echo
        echo "##"
        echo "## Validating production file in $folder"
        echo "##"
        python $folder/validate.py $folder/production.json
    else
        echo "##"
        echo "## No validator found for $folder, skipping"
        echo "##"
    fi
    echo
done

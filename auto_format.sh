#!/bin/bash

find . -name "*.py" | xargs -I{} -P 4 bash -c 'echo "Processing {}"; autopep8 --in-place --aggressive --aggressive {}'
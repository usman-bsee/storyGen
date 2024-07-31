#!/bin/bash

# Check for running Docker container
if docker container ls | grep ocr-extraction > /dev/null ; then
    echo "Running flake8 in Docker container..."
    docker exec -it ocr-extraction flake8
else
    # Check if flake8 is installed
    if ! command -v flake8 &> /dev/null; then
        echo "The Docker container is not running and flake8 is not installed locally."
        read -p "Would you like to install flake8? (y/n) " yn
        case $yn in
            [Yy]* ) pip install flake8;;
            [Nn]* ) echo "Please run the docker container or install flake8 locally."; exit;;
            * ) echo "Please answer yes or no."; exit;;
        esac
    fi
    flake8
fi
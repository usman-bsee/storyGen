#!/bin/bash


echo script Started at $(date) value of text : $(cat /home/ubuntu/storyGen/celery-on.txt) >> /home/ubuntu/storyGen/logs_script.txt
sleep 10
while true; do
  if [ -f /home/ubuntu/storyGen/celery-on.txt ] && [ $(cat /home/ubuntu/storyGen/celery-on.txt) == "1" ]; then
    echo "Starting Celery worker..."
    echo script Loaded Celery at $(date) value of text : $(cat /home/ubuntu/storyGen/celery-on.txt) >> /home/ubuntu/storyGen/logs_script.txt
    celery -A tasks worker --loglevel=info -c 1
    # exit 0
  fi
  echo "sleeping for one sec " $(cat /home/ubuntu/storyGen/celery-on.txt)
  
  sleep 1
done

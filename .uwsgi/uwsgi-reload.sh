#!/bin/bash 

nc -l 9025 -k > /var/tubmanproject.test/api/.uwsgi/reload-file

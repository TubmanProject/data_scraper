#!/bin/bash

fswatch -v -o /Users/tyronesaunders/projects/tubmanproject/chef/api | xargs -n1 -I{} echo 'restart' | nc localhost 9025 > /dev/null &
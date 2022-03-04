#!/bin/bash

/home/ray/branch/venv/bin/python3 -m datasette serve /home/ray/branch/my-app/ -h 127.0.0.1 -p 8010 --crossdb

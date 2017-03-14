#!/bin/bash

pip install -r requirements.txt -t lib
dev_appserver.py --host 0.0.0.0 .


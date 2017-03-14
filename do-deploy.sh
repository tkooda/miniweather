#!/bin/bash

#gcloud auth list

gcloud app deploy --project=miniweather-1 app.yaml

# gcloud app logs tail -s default

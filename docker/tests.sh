#!/usr/bin/env bash

set -e

echo "Tests..."

NOTEBOOK_NAME=test python run.py

if [[ -f /output/test.ipynb ]]; then
    echo "."
else
    echo "Error! /output/test.ipynb not found."
fi

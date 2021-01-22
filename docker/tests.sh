#!/usr/bin/env bash

set -e

echo "Tests..."

NOTEBOOK_NAME=test python run.py

if [[ -f /output/test.ipynb ]]; then
    echo "."
else
    echo "Error! /output/test.ipynb not found."
fi

NOTEBOOK_NAME=test PARAM_var1=3.1415 PARAM_var2="'Hello Test!'" python run.py

if grep -q "var1 = 3.1415" /output/test.ipynb; then
    echo "."
else
    echo "Error! Incorrect output in /output/test.ipynb."
fi

if grep -q "var2 = Hello Test!" /output/test.ipynb; then
    echo "."
else
    echo "Error! Incorrect output in /output/test.ipynb."
fi

if grep -q "Type var1 = <class 'float'>" /output/test.ipynb; then
    echo "."
else
    echo "Error! Incorrect type in /output/test.ipynb."
fi

if grep -q "Type var2 = <class 'str'>" /output/test.ipynb; then
    echo "."
else
    echo "Error! Incorrect type in /output/test.ipynb."
fi

NOTEBOOK_NAME=test PARAMETERS='{"var1": 1234.5, "var2": "It works!"}' python run.py

if grep -q "var1 = 1234.5" /output/test.ipynb; then
    echo "."
else
    echo "Error! Incorrect output in /output/test.ipynb."
fi

if grep -q "var2 = It works!" /output/test.ipynb; then
    echo "."
else
    echo "Error! Incorrect output in /output/test.ipynb."
fi

if grep -q "Type var1 = <class 'float'>" /output/test.ipynb; then
    echo "."
else
    echo "Error! Incorrect type in /output/test.ipynb."
fi

if grep -q "Type var2 = <class 'str'>" /output/test.ipynb; then
    echo "."
else
    echo "Error! Incorrect type in /output/test.ipynb."
fi

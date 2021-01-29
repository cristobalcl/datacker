#!/usr/bin/env bash

set -e

echo "Tests..."

NOTEBOOK_NAME=test python -m datacker_runner.run

if [[ -f /output/*_test.ipynb ]]; then
    echo "."
else
    echo "Error! /output/*_test.ipynb not found."
fi

NOTEBOOK_NAME=test PARAM_var1=3.1415 PARAM_var2="'Hello Test!'" python -m datacker_runner.run

if grep -q "var1 = 3.1415" /output/*_test.ipynb; then
    echo "."
else
    echo "Error! Incorrect output in /output/*_test.ipynb."
fi

if grep -q "var2 = Hello Test!" /output/*_test.ipynb; then
    echo "."
else
    echo "Error! Incorrect output in /output/*_test.ipynb."
fi

if grep -q "Type var1 = <class 'float'>" /output/*_test.ipynb; then
    echo "."
else
    echo "Error! Incorrect type in /output/*_test.ipynb."
fi

if grep -q "Type var2 = <class 'str'>" /output/*_test.ipynb; then
    echo "."
else
    echo "Error! Incorrect type in /output/*_test.ipynb."
fi

NOTEBOOK_NAME=test PARAMETERS='{"var1": 1234.5, "var2": "It works!"}' python -m datacker_runner.run

if grep -q "var1 = 1234.5" /output/*_test.ipynb; then
    echo "."
else
    echo "Error! Incorrect output in /output/*_test.ipynb."
fi

if grep -q "var2 = It works!" /output/*_test.ipynb; then
    echo "."
else
    echo "Error! Incorrect output in /output/*_test.ipynb."
fi

if grep -q "Type var1 = <class 'float'>" /output/*_test.ipynb; then
    echo "."
else
    echo "Error! Incorrect type in /output/*_test.ipynb."
fi

if grep -q "Type var2 = <class 'str'>" /output/*_test.ipynb; then
    echo "."
else
    echo "Error! Incorrect type in /output/*_test.ipynb."
fi

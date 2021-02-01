#!/usr/bin/env bash

set -e

echo "Tests"

NOTEBOOK_NAME=test OUTPUT_PREFIX="" python -m datacker_runner.run

if [[ -f /output/test.ipynb ]]; then
    echo "."
else
    echo "Error! /output/test.ipynb not found."
    exit 1
fi

NOTEBOOK_NAME=test PARAM_var1=3.1415 PARAM_var2="'Hello Test!'" OUTPUT_PREFIX="" python -m datacker_runner.run

if grep -q "var1 = 3.1415" /output/test.ipynb; then
    echo "."
else
    echo "Error! Incorrect output in /output/test.ipynb."
    exit 1
fi

if grep -q "var2 = Hello Test!" /output/test.ipynb; then
    echo "."
else
    echo "Error! Incorrect output in /output/test.ipynb."
    exit 1
fi

if grep -q "Type var1 = <class 'float'>" /output/test.ipynb; then
    echo "."
else
    echo "Error! Incorrect type in /output/test.ipynb."
    exit 1
fi

if grep -q "Type var2 = <class 'str'>" /output/test.ipynb; then
    echo "."
else
    echo "Error! Incorrect type in /output/test.ipynb."
    exit 1
fi

NOTEBOOK_NAME=test PARAMETERS='{"var1": 1234.5, "var2": "It works!"}' OUTPUT_PREFIX="" python -m datacker_runner.run

if grep -q "var1 = 1234.5" /output/test.ipynb; then
    echo "."
else
    echo "Error! Incorrect output in /output/test.ipynb."
    exit 1
fi

if grep -q "var2 = It works!" /output/test.ipynb; then
    echo "."
else
    echo "Error! Incorrect output in /output/test.ipynb."
    exit 1
fi

if grep -q "Type var1 = <class 'float'>" /output/test.ipynb; then
    echo "."
else
    echo "Error! Incorrect type in /output/test.ipynb."
    exit 1
fi

if grep -q "Type var2 = <class 'str'>" /output/test.ipynb; then
    echo "."
else
    echo "Error! Incorrect type in /output/test.ipynb."
    exit 1
fi

if NOTEBOOK_NAME=test PARAM_var2="'TEST_STRING'" OUTPUT_STDOUT=true OUTPUT_PREFIX="" python -m datacker_runner.run | grep var2 | grep TEST_STRING; then
    echo "."
else
    echo "Error! No output detected from stdout."
    exit 1
fi

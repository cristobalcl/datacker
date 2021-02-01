#!/usr/bin/env python3

import sys
import os
from datetime import datetime
from ast import literal_eval
import json
from pathlib import Path

import papermill as pm


PARAMETER_PREFIX = "PARAM_"


def get_config(environment) -> dict:
    config = {
        "NOTEBOOK_NAME": environment.get("NOTEBOOK_NAME", "main"),
        "NOTEBOOKS_PATH": Path(environment.get("NOTEBOOKS_PATH", "/notebooks/")),
        "OUTPUT_PATH": Path(environment.get("OUTPUT_PATH", "/output/")),
        "OUTPUT_PREFIX": environment.get("OUTPUT_PREFIX", "%Y%m%d%H%M%S%f_"),
        "OUTPUT_STDOUT": environment.get("OUTPUT_STDOUT", "false") == "true",
    }
    return config


def get_parameters(environment) -> dict:
    parameters = json.loads(environment.get("PARAMETERS", "{}"))
    for key, value in environment.items():
        if not key.startswith(PARAMETER_PREFIX):
            continue
        parameters[key.split(PARAMETER_PREFIX, 1)[-1]] = literal_eval(value)
    return parameters


def run(parameters, config):
    notebook_name = config["NOTEBOOK_NAME"]
    output_prefix = datetime.utcnow().strftime(config["OUTPUT_PREFIX"])
    output_filename = config["OUTPUT_PATH"] / f"{output_prefix}{notebook_name}.ipynb"

    pm.execute_notebook(
        config["NOTEBOOKS_PATH"] / f"{notebook_name}.ipynb",
        output_filename,
        parameters=parameters,
    )

    if config["OUTPUT_STDOUT"]:
        with open(output_filename) as f:
            print(f.read())


def main() -> int:
    config = get_config(os.environ)
    parameters = get_parameters(os.environ)
    run(parameters, config)

    return 0


if __name__ == "__main__":
    sys.exit(main())

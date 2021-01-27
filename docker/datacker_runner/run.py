#!/usr/bin/env python3

import sys
import os
from datetime import datetime
from ast import literal_eval
import json
from pathlib import Path

import papermill as pm


PARAMETER_PREFIX = "PARAM_"


def get_parameters(environment):
    parameters = json.loads(environment.get("PARAMETERS", "{}"))
    for key, value in environment.items():
        if not key.startswith(PARAMETER_PREFIX):
            continue
        parameters[key.split(PARAMETER_PREFIX, 1)[-1]] = literal_eval(value)
    return parameters


def main() -> int:
    notebooks_path = Path("/notebooks/")
    output_path = Path("/output/")
    notebook_name = os.environ["NOTEBOOK_NAME"]
    parameters = get_parameters(os.environ)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    pm.execute_notebook(
        notebooks_path / f"{notebook_name}.ipynb",
        output_path / f"{timestamp}_{notebook_name}.ipynb",
        parameters=parameters,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())

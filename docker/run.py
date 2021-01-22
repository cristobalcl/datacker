#!/usr/bin/env python3

import sys
import os
from pathlib import Path

import papermill as pm


def main():
    notebooks_path = Path("/notebooks/")
    output_path = Path("/output/")
    notebook_name = os.environ["NOTEBOOK_NAME"]
    pm.execute_notebook(
        notebooks_path / f"{notebook_name}.ipynb",
        output_path / f"{notebook_name}.ipynb",
        parameters=dict(),
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())

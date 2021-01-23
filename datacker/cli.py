from typing import List
from pathlib import Path

import typer

from . import build_datacker


app = typer.Typer()


@app.command()
def main(image_name: str, notebooks: List[str]):
    build_datacker(
        image_name, [Path(notebook) for notebook in notebooks],
    )


if __name__ == "__main__":
    app()

from typing import List

import typer

from .builder import DatackerBuilder


app = typer.Typer()


@app.command()
def main(image_name: str, notebooks: List[str]):
    builder = DatackerBuilder(image_name, notebooks)
    builder.build()


if __name__ == "__main__":
    app()

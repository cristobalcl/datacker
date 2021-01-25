from typing import List

import typer

from .builder import DatackerBuilder


app = typer.Typer()


@app.command()
def main(
    image_name: str,
    notebooks: List[str],
    requirements_file: str = typer.Option(  # noqa: B008
        None,
        "--requirements",
        "-r",
        help="Path to requirements file",
        show_default=False,
    ),
):
    builder = DatackerBuilder(
        image_name, list(notebooks), requirements_file=requirements_file
    )
    builder.build()

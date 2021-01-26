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
    image_name_styled = typer.style(image_name, fg=typer.colors.GREEN, bold=True)
    typer.echo(f"Create image {image_name_styled} with notebooks:")
    typer.echo()
    for notebook in notebooks:
        notebook_styled = typer.style(notebook, fg=typer.colors.BLUE, bold=True)
        typer.echo(f" → {notebook_styled}")
    typer.echo()
    builder = DatackerBuilder(
        image_name, list(notebooks), requirements_file=requirements_file
    )
    typer.echo("Building...")
    typer.echo()
    builder.build()
    typer.secho("Done!", fg=typer.colors.GREEN, bold=True)

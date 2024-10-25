import typer

from project import settings
from scripts.introspection import extract__all__from_submodules


app = typer.Typer()


@app.command()
def dump_settings(json: bool = False) -> None:
    from project.store import store

    # load all the module settings to make sure store contain all the variables
    extract__all__from_submodules(settings)

    if json:
        typer.echo(store.dump_jsonl())
    else:
        typer.echo(store.dump_markdown())


@app.command()
def test() -> None:
    typer.echo("Running tests...")


if __name__ == "__main__":
    app()

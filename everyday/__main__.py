import webbrowser

import click

from everyday import config, create_app


@click.group()
def cli():
    pass


@cli.command()
@click.option("--debug", "-d", is_flag=True)
def run(debug):
    app = create_app(config)
    if not debug:
        webbrowser.open(f"http://localhost:{config.PORT}")

    app.run(debug=debug, port=config.PORT)

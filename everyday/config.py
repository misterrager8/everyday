import os
import pathlib

import click
import dotenv

dotenv.load_dotenv()

HOME_DIR, PORT = None, None

try:
    PORT = os.getenv("port") or "5009"
    HOME_DIR = pathlib.Path(
        os.getenv("home_dir") or pathlib.Path(__file__).parent.parent / "Journals"
    )

    if not HOME_DIR.exists():
        HOME_DIR.mkdir()
except Exception as e:
    click.secho(str(e), fg="red")

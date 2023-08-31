"""Basic script to symlink src/disnake/ext/oauth2 into the current python env."""
# thanks sharp and disnake-ext-components for this :pray:

import pathlib
import sys
import typing

import disnake

_DEST = (pathlib.Path(disnake.__file__).parent / "ext" / "oauth2").resolve()
_SOURCE = (pathlib.Path.cwd() / "src" / "disnake" / "ext" / "oauth2").resolve()


def _main() -> typing.NoReturn:
    if not _DEST.exists():
        _DEST.symlink_to(_SOURCE)
        print(f"Successfully set up symlink from '{_SOURCE}' to '{_DEST}'!")

    else:
        print(f"{_DEST!r} already exists. Skipping.")

    sys.exit(0)


if __name__ == "__main__":
    _main()

"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Ham Ibp Monitor."""


if __name__ == "__main__":
    main(prog_name="ham-ibp-monitor")  # pragma: no cover
